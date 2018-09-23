import scrapy


class UsersSpider(scrapy.Spider):
	name = 'users'

	custom_settings = {
		'JOBDIR': 'crawls/users-1',
	}

	start_urls = ['https://www.facebook.com/zuck']

	# def start_requests(self):
	# 	_from = getattr(self, 'from', 4)
	# 	to = getattr(self, 'to', 5)

	# 	for id in range(int(_from), int(to) + 1):
	# 		yield scrapy.Request('https://www.facebook.com/profile.php?id={}'.format(id))

	def parse(self, response):
		relevent_users = response.xpath('//div[@class="profileFriendsText"]//a/@href').extract()

		for relevent_user in relevent_users:
			yield scrapy.Request(relevent_user)

		name = response.xpath('//*[@id="fb-timeline-cover-name"]/a/text()').extract_first()
		image = response.xpath('//*[contains(@class, "profilePicThumb")]//img/@src').extract_first()
		is_verified = bool(response.xpath('//*[@id="fbProfileCover"]//*[@data-hover="tooltip"]').extract())

		images = response.xpath('//*[@id="profile_photos_unit"]//img/@src').extract()

		_education_work = response.xpath('//*[@id="pagelet_eduwork"]')
		_residency = response.xpath('//*[@id="pagelet_hometown"]')

		# Work & Educations
		_work_container = response.xpath('.//*[contains(text(), "Work")]/../../ul[contains(@class, "uiList fbProfileEditExperiences")]')
		_education_container = response.xpath('.//*[contains(text(), "Education")]/../../ul[contains(@class, "uiList fbProfileEditExperiences")]')

		# Work
		works = []

		if _work_container:
			for _work in _work_container[0].xpath('.//li[contains(@class, "fbEditProfileViewExperience")]'):
				works.append({
					'url': _work.xpath('.//*[@class="_2lzr _50f5 _50f7"]//a/@href').extract_first(),
					'place': _work.xpath('.//*[@class="_2lzr _50f5 _50f7"]//a/text()').extract_first(),
					'more': _work.xpath('.//*[@class="fsm fwn fcg"]//text()').extract()
				})

		# Educations
		educations = []

		if _education_container:
			for _education in _education_container[0].xpath('.//li[contains(@class, "fbEditProfileViewExperience")]'):
				educations.append({
					'url': _education.xpath('.//*[@class="_2lzr _50f5 _50f7"]//a/@href').extract_first(),
					'place': _education.xpath('.//*[@class="_2lzr _50f5 _50f7"]//a/text()').extract_first(),
					'more': _education.xpath('.//*[@class="fsm fwn fcg"]//text()').extract()
				})

		# Home Town
		_residency_container = response.xpath('.//*[contains(text(), "Current City and Home Town")]/../../ul[contains(@class, "uiList fbProfileEditExperiences")]')

		residencies = []

		if _residency_container:
			for _residency in _residency_container[0].xpath('.//li[contains(@class, "fbEditProfileViewExperience")]'):
				residencies.append({
					'url': _residency.xpath('.//*[@class="_2lzr _50f5 _50f7"]//a/@href').extract_first(),
					'place': _residency.xpath('.//*[@class="_2lzr _50f5 _50f7"]//a/text()').extract_first(),
					'more': _residency.xpath('.//*[@class="fsm fwn fcg"]//text()').extract()
				})

		# id="pagelet_pronounce"
		bio = response.xpath('//*[@id="pagelet_bio"]//*[@class="_c24 _2iem"]//text()').extract()
		nicknames = response.xpath('//*[@id="pagelet_nicknames"]//text()').extract()
		quotes = response.xpath('//*[@id="pagelet_quotes"]//*[@class="_4bl9"]//text()').extract()

		_favourites = response.xpath('//table[@class="mtm _5e7- profileInfoTable _3stp _3stn"]')

		favourites = []

		for _favourite in _favourites.xpath('.//tr'):
			favourites.append({
				'key': _favourites.xpath('.//div[@class="labelContainer"]//text()').extract_first(),
				'value': _favourites.xpath('.//div[@class="mediaPageName"]//text()').extract_first(),
			})

		_contacts = response.xpath('//*[@id="contact_info"]')

		contacts = []

		for _contact in _contacts.xpath('.//li'):
			contacts.append({
				'medium': _contact.xpath('.//*[@role="heading"]//text()').extract_first(),
				'value': _contact.xpath('.//*[@class="_4bl7 _pt5"]//text()').extract(),
			})

		yield {
			'name': name,
			'profile_picture': image,
			'images': images,
			'is_verified': is_verified,
			'works': works,
			'educations': educations,
			'home_town': residencies,
			'quotes': quotes,
			'favourites': favourites,
			'nicknames': nicknames,
			'bio': bio,
			'contacts': contacts,
		}
