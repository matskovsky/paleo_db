from __future__ import unicode_literals

from django.conf import settings
from datetime import date
from django.contrib.auth.models import User, Group
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.core.exceptions import ValidationError

# ---- Валидатор полей "Год" ------------------------------------------------------------#######
def validate_year(value):
	if not (int(value) > 1600 and int(value) <= date.today().year+1):
		raise ValidationError(
			'Значение "%(value)" не является годом',
			params={'value': value},
		)


#####-------  Абстрактный класс для задания прав доступа к объектам БД ------------------#######
class PINAccessModel(models.Model):
	# -------- технические поля для доступа и т.п. ---------------------------
	user_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.PROTECT) # пользователь, владелец модели, который может ее редактировать
	group_owner = models.ForeignKey(Group, related_name='+', on_delete=models.PROTECT) # группа, владелец модели, члены этой группы могут ее редактировать (например, лаборатория беспозвоночных. Сделано для возможности поддержки отдельных частей БД, доступных для просмотра и редактирования только конкретной лабораторией)
	status_accepted = models.SmallIntegerField(default=0) # вспомогательное поле, для задания статуса присоединения к общей базе (0 - не входит в общую БД, 1 - входит)
	status_published = models.SmallIntegerField(default=0) # вспомогательное поле, для задания статуса возможности просмотра (0 - просмотр закрыт, 1 - просмотр для внутреннего пользования, 2 - просмотр для всех)

	class Meta:
		abstract = True


#####-------  Модель Организации ----------------------------------------------------#######
class Organization(PINAccessModel):
	name = models.CharField(max_length=64, null=True)
	shortName = models.CharField(max_length=64, null=True)
	alternateName = models.CharField(max_length=64, null=True)
	contacts = models.CharField(max_length=256, null=True)


#####-------  Модель Лаборатории ----------------------------------------------------#######
class Lab(PINAccessModel):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	name = models.CharField(max_length=64, null=True)
	shortName = models.CharField(max_length=64, null=True)
	alternateName = models.CharField(max_length=64, null=True)
	contacts = models.CharField(max_length=256, null=True)


#####-------  Модель Персоны --------------------------------------------------------#######
class Person(PINAccessModel):
	firstName = models.CharField(max_length=64, null=True) # имя
	middleName = models.CharField(max_length=64, null=True) # отчество
	lastName = models.CharField(max_length=64) # фамилия
	alternateName = models.CharField(max_length=64, null=True) # другие имена (например, при смене фамилии)
	firstNameLatin = models.CharField(max_length=64, null=True) # имя латинское
	middleNameLatin = models.CharField(max_length=64, null=True) # отчество латинское
	lastNameLatin = models.CharField(max_length=64, null=True) # фамилия латинское
	alternateNameLatin = models.CharField(max_length=64, null=True) # другие имена (например, при смене фамилии) латинское
	contacts = models.CharField(max_length=256, null=True) # контакты
	email =  models.EmailField(max_length=254, null=True) # email, если есть, может быть использован для автоматических оповещений
	organizations = models.ManyToManyField(Organization) # организации работы

	# ---- Метод для получения сокращенного имени (с инициалами) ------
	def get_short_name(self):
		pass



#####-------  Модель Группы персон --------------------------------------------------#######
class PersonsGroup(models.Model):
	persons = models.ManyToManyField(Person, through='Authorship')


#####-------  Промежуточная модель для авторства ------------------------------------#######
class Authorship(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE) # автор
	group = models.ForeignKey(PersonsGroup, on_delete=models.CASCADE) # группа авторов
	order = models.SmallIntegerField(default=1, null=False) # используется для упорядочивания авторов


#####-------  Модель Издания ----------------------------------------------------#######
class Periodical(PINAccessModel):
	name = models.CharField(max_length=128, null=True)
	shortName = models.CharField(max_length=64, null=True)
	alternateName = models.CharField(max_length=128, null=True)
	info = models.CharField(max_length=256, null=True)



#####-------  Модель Публикации -----------------------------------------------------#######
class Publication(PINAccessModel):
	authors = models.ForeignKey(PersonsGroup, on_delete=models.CASCADE)	 # авторы
	authors_text = models.CharField(max_length=512, null=True)	 # авторы, текстовое поле до заполнения всех связей
	year = models.CharField(max_length=4, validators=[validate_year]) # год
	title = models.CharField(max_length=512, null=True) # название
	titleLatin = models.CharField(max_length=512, null=True) # название латинское
	periodical = models.ForeignKey(Periodical, on_delete=models.CASCADE, null=True) #издание
	periodical_text = models.CharField(max_length=128, null=True) #издание, текстовое поле до заполнения всех связей
	series = models.CharField(max_length=128, null=True) # серия
	volume = models.CharField(max_length=32, null=True) # том/номер
	issue = models.CharField(max_length=32, null=True) # выпуск
	issueTitle = models.CharField(max_length=128, null=True) # название сборника
	editors = models.ForeignKey(PersonsGroup, related_name='editors', on_delete=models.CASCADE, null=True) # редакторы
	editors_text = models.CharField(max_length=128, null=True) # редакторы в текстовом виде
	city = models.CharField(max_length=64, null=True) # город
	publisher = models.CharField(max_length=128, null=True) # издательство
	pages = models.CharField(max_length=128, null=True) # страницы, кол-во таблиц, иллюстраций и т.п.
	group = models.CharField(max_length=64, null=True) # группа организмов
	notes = models.CharField(max_length=512, null=True) # примечание (+ поле ИСХОДНОЙ БАЗЫ - "хранится")
	shelfCodeUp = models.CharField(max_length=20, null=True) # шифр (верх)
	shelfCodeDown = models.CharField(max_length=20, null=True) # шифр (низ)

	# ---- Метод для получения сокращенного списка авторов (1-2 автора с инициалами) ------
	def get_short_authors(self, latin=False):
		pass

#####-------  Модель для геолокации --------------------------------------------------#######
class geoLocation(models.Model):
	center = models.CharField(max_length=44, null=True) # рассчитанный центр объекта, пара координат в формате geoJSON
	extent = models.CharField(max_length=84, null=True) # рассчитанные границы объекта, четыре координаты в формате geoJSON
	geoJSON = models.TextField(null=True) # геометрия объекта в формате geoJSON
	description = models.CharField(max_length=256, null=True) # описание

	# ---- Метод для рассчета центра ------
	def _get_center(self):
		pass

	# ---- Метод для рассчета границ ------
	def _get_extent(self):
		pass

	# ---- Метод для изменения/создания объекта с расчетом границ и центра ------
	def save(self, force_insert=False):
		if self.center is None or self.center == '':
			self.center = self._get_center()

		if self.extent is None or self.extent == '':
			self.extent = self._get_extent()

		return super(geoLocation, self).save(force_insert=force_insert)


#####-------  Модель для места хранения ----------------------------------------------#######
class storageLocation(MPTTModel, PINAccessModel):
	STICKER_SIZE = (
		('01', 'размер 1'),
		('02', 'размер 2'),
		('03', 'размер 3'),
		('04', 'размер 4'),
		('05', 'размер 5'),
		('06', 'размер 6'),
		('07', 'размер 7'),
		('08', 'размер 8'),
		('09', 'размер 9'),
		('10', 'размер 10'),
		('11', 'размер 11'),
		('12', 'размер 12'),
		('22', 'размер 22'),
		('91', 'размер 91'),
		('00', 'не определен'),
	) # размер наклейки на ящик/лоток

	name = models.CharField(max_length=64)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
	description = models.CharField(max_length=256, null=True) # описание
	stickerSize = models.CharField(max_length=2, choices=STICKER_SIZE, default='00', null=True) # размер наклейки на ящик/лоток

	class Meta:
		unique_together = (('parent','name',),)


	class MPTTMeta:
		order_insertion_by = ['name']


#####-------  Модель для едиа материалов----------------------------------------------#######
class Media(models.Model):
	pass


#####-------  Модель Коллекции ----------------------------------------------------------#######
class Collection(PINAccessModel):
	id = models.IntegerField(default=0, primary_key=True)
	number = models.IntegerField(default=0, null=False, unique=True) # Номер коллекции
	dateRegistered = models.DateField(null=True, default=date.today) # Дата регистрации
	dateRegistered_precision = models.CharField(max_length=40, null=True) # Дополнительное поле для поддержки неформатных дат регистрации. Примеры значений: month, year (точноть - месяц, год), year_3 (период продолжительностью 3 года, начиная с указанного), year_before (до указанного года). Также возможен произвольный текст (например, 1959?)
	content = models.CharField(max_length=256, null=True) # содержание коллекции
	stratigraphicUnit= models.CharField(max_length=256, null=True) # стратон - система, отдел, ярус и т.д. (в случае неразделенных стратонов – через тире) (В ИСХОДНОЙ БАЗЕ - "Возраст")
	collectors = models.ManyToManyField(PersonsGroup) # коллекторы
	collectors_text = models.CharField(max_length=256, null=True) # коллекторы, текстовое поле. Используется как временное до полного заполнения персоналий и использования их как коллекторов
	location = models.TextField(null=True) # местонахождение происхождения коллекции (В ИСХОДНОЙ БАЗЕ - "Регион")
	geoLocations = models.ManyToManyField(geoLocation) # геолокации
	collectYears = models.CharField(max_length=128, null=True) # годы сбора коллекции  ############# !!!!! ПОДУМАТЬ ПРО ПОИСК!!!!!!!! - таблица небольшая, т.ч. можно сделать полнотекстовый поиск при вводе года или периода.
	organizations = models.ManyToManyField(Organization) # организации
	organizations_text = models.CharField(max_length=256, null=True) # организации, текстовое поле до заполнения всех связей
	quantity = models.CharField(max_length=128, null=True) # количество
	labs = models.ManyToManyField(Lab) # лаборатории, ответственные за коллекцию
	labs_text = models.CharField(max_length=256, null=True) # лаборатории, текстовое поле до заполнения всех связей
	notes = models.CharField(max_length=512, null=True) # примечание
	responsiblePersons = models.ManyToManyField(Person) # персона(ы), ответственная(ые) за коллекцию

	# class Meta:
		# permissions = (
			# ("view_collection", "Can see available collections"),
			# ("change_collection_status_accepted", "Can change the status_accepted of collections"),
			# ("change_collection_status_published", "Can change the status_published of collections"),
			# ("edit_collection", "Can edit collections"),
		# )	# права доступа


#####-------  Модель Таксона -------------------------------------------------------#######
class Taxon(PINAccessModel):
	group = models.CharField(max_length=128, null=True) # группа организмов
	genus = models.CharField(max_length=128, null=True) # род
	subgenus = models.CharField(max_length=128, null=True) # подрод
	species = models.CharField(max_length=128, null=True) # вид
	speciesAuthor = models.CharField(max_length=128, null=True) # автор вида
	speciesYear = models.CharField(max_length=4, validators=[validate_year], null=True) # год выделения вида
	subspecies = models.CharField(max_length=128, null=True) # подвид
	subspeciesAuthor = models.CharField(max_length=128, null=True) # автор подвида
	subspeciesYear = models.CharField(max_length=4, null=True, validators=[validate_year]) # год выделения подвида


#####-------  Модель Экземпляра------------------------------------------------------#######
class Sample(PINAccessModel):
	number = models.CharField(max_length=64, blank=False, null=False, default='') # Номер экземпляра в коллекции
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE) # коллекция
	publications = models.ManyToManyField(Publication, through='Description') # публикации, описывающие экземпляр
	country = models.CharField(max_length=128, null=True) # страна
	region = models.CharField(max_length=128, null=True) # регион (В ИСХОДНОЙ БАЗЕ - "Область")
	regionSpec = models.CharField(max_length=128, null=True) # уточнение региона (В ИСХОДНОЙ БАЗЕ - "Регион")
	geologicalContext = models.CharField(max_length=256, null=True) # структура
	location = models.CharField(max_length=512, null=True) # местонахождение (максимально подробное, уточненное)
	verbatimLocation = models.CharField(max_length=512, null=True) # исходное текстовое описание местонахождения
	geoLocations = models.ManyToManyField(geoLocation) # геолокации
	sistema = models.CharField(max_length=256, null=True) # система
	yarus = models.CharField(max_length=256, null=True) # ярус
	gorizont = models.CharField(max_length=256, null=True) # горизонт
	svita = models.CharField(max_length=256, null=True) # свита
	sloy = models.CharField(max_length=256, null=True) # слой
	type = models.CharField(max_length=256, null=True) # природа образца
	dateCollected = models.DateField(null=True) # Год сборов
	dateCollected_precision = models.CharField(max_length=40, null=True) # Дополнительное поле для поддержки неформатного года сбора. Примеры значений: см. аналог в Collection
	responsiblePersons = models.ManyToManyField(Person) # персона(ы), ответственная(ые) за экземпляр
	storageLocation = models.ForeignKey(storageLocation, on_delete=models.CASCADE, null=True)	 # место хранения
	storageLocation_text = models.CharField(max_length=128, null=True)	 # место хранения - текстовое поле до заполнения всех связей (В ИСХОДНОЙ БАЗЕ - "Шкаф/лоток")
	is_stored = models.NullBooleanField(default=True, null=True) # в наличии / отсутствует
	notes = models.CharField(max_length=512, null=True) # примечание
	stickerSize = models.CharField(max_length=32, null=True) # размер наклейки на ящик/лоток ################# !!!!!!!!!!!!!!!!!!!!!!!!!! временно, перенос на SrorageLocation !!!!!!!!!!!!!
	relatedMedia = models.ManyToManyField(Media) # медиа материалы
	id_old_DB = models.IntegerField(default=0, unique=True) # id из старой базы Access на всякий случай

	class Meta:
		unique_together = (('collection','number',),)


#####-------  Промежуточная модель для описания экземпляра в публикации ----------------#######
class Description(models.Model):
	TYPE = (
		('frst', 'первоописание'),
		('next', 'переописание'),
		('othr', 'другое'),
	) # тип публикации

	NEW_TAXON = (
		('sn', 'sp. nov.'),
		('ssn', 'subsp. nov.'),
		('sgsn', 'subgen. et sp. nov.'),
		('gn', 'gen. nov.'),
		('gsn', 'gen. et sp. nov.'),
		('nn', 'nom. nov.'),
		('vn', 'var. nov.'),
		('nul', 'не указано'),
	) # новый таксон

	CAT = (
		('hlt', 'голотип'),
		('dbl', 'дублет'),
		('lkt', 'лектотип'),
		('ntp', 'неотип'),
		('org', 'оригинал'),
		('plt', 'паралектотип'),
		('prt', 'паратип'),
		('snt', 'синтип'),
		('nul', 'не определен'),
	) # категория экземпляра

	sample = models.ForeignKey(Sample, on_delete=models.CASCADE) # автор
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=True) # публикация, в которой дано это описание
	taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE) # описано данным таксоном
	newTaxon = models.CharField(max_length=4, choices=NEW_TAXON, default='nul') # новый таксон
	publication_type = models.CharField(max_length=4, choices=TYPE, default='othr') # тип публикации
	category = models.CharField(max_length=3, choices=CAT, default='nul') # категория
	citation = models.CharField(max_length=512, null=True) # ссылка на экземпляр в публикации
	storage_indicated = models.NullBooleanField(default=True, null=True) # указано ли хранение в публикации (В ИСХОДНОЙ БАЗЕ - "хран в указ/раб")
	notes = models.CharField(max_length=512, null=True) # примечание

	########### --------------- ВРЕМЕННЫЕ ПОЛЯ, ПОКА НЕ СОЗДАНЫ И НЕ ЗАПОЛНЕНЫ ТАКСОНЫ ----------- !!!!!!!!!!!!!!!!! -----------
	group = models.CharField(max_length=128, null=True) # группа организмов
	genus = models.CharField(max_length=128, null=True) # род
	subgenus = models.CharField(max_length=128, null=True) # подрод
	species = models.CharField(max_length=128, null=True) # вид
	speciesAuthor = models.CharField(max_length=128, null=True) # автор вида
	speciesYear = models.CharField(max_length=4, validators=[validate_year], null=True) # год выделения вида
	subspecies = models.CharField(max_length=128, null=True) # подвид
	subspeciesAuthor = models.CharField(max_length=128, null=True) # автор подвида
	subspeciesYear = models.CharField(max_length=4, null=True, validators=[validate_year]) # год выделения подвида


#####-------  Модель Акта приемки -------------------------------------------------#######
class Act(PINAccessModel):
	id = models.IntegerField(default=0, primary_key=True) # Номер акта
	dateAcquired = models.DateField(null=True, default=date.today) # Дата приема
	group = models.CharField(max_length=64, null=True) # группа организмов
	stratigraphicUnit= models.CharField(max_length=256, null=True) # стратон - система, отдел, ярус и т.д. (в случае неразделенных стратонов – через тире) (В ИСХОДНОЙ БАЗЕ - "Возраст")
	collections = models.ManyToManyField(Collection) # принятые коллекции
	collections_text = models.CharField(max_length=128, null=True) # принятые коллекции - текстовое поле до заполнения всех связей (В ИСХОДНОЙ БАЗЕ - "колл №№")
	samples = models.ManyToManyField(Sample) # принятые экземпляры (возможно, до этого никогда не дойдет)
	sampleCount = models.CharField(max_length=64, null=True) # сколько принято экземпляров - текстовое поле до заполнения всех связей (В ИСХОДНОЙ БАЗЕ - "экземпляров")
	storageLocation = models.ForeignKey(storageLocation, on_delete=models.CASCADE, null=True)	 # место хранения
	storageLocation_text = models.CharField(max_length=128, null=True)	 # место хранения - текстовое поле до заполнения всех связей
	publications = models.ManyToManyField(Publication) # относящиеся к принятым экземплярам публикации ????????????????????????????????????????????????
