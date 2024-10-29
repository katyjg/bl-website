from django.core.management.base import BaseCommand, CommandError

from wagtail.models import Page, Site
from wagtail.images.models import Image
from wagtailmenus.models import MainMenu, MainMenuItem

from beamol.news.models import NewsPage, PostPage, PostCategory, Tag
from beamol.home.models import HomePage
from beamol.beamlines.models import BeamlinePage, PublicationsPage


class Command(BaseCommand):
    help = 'Creates test pages for a beamline website. Only to be run on a clean database.'

    def add_arguments(self, parser):
        parser.add_argument('--beamline', type=str)

    def handle(self, *args, **options):
        if Page.objects.all().count() > 2:
            return "Unable to create test site. Pages already exist."

        beamline = options.get('beamline') or 'Mid-IR'
        Page.objects.exclude(pk=Page.objects.first().get_root().pk).delete()

        rootpage = Page.objects.first()

        # Create Images
        images = {}
        for img in ["crystal-background.jpg", "logo.png", "pattern.png"]:
            images[img] = Image(title=img.split('.')[0].title(), file="original_images/{}".format(img))
            images[img].save()

        homeinfo = {
            "call": "<h2>Access our Beamline</h2><p><a href=\"https://confluence.lightsource.ca/display/CMCF/CMCF+Website+Release+Notes\">Docs</a></p><p>Learn more about the website in the docs.</p>",
            "announcements": "<p>An optional announcement bar</p>",
            "footer1": "<h4>Some Footer Content:</h4><p>Can go here</p>",
            "footer2": "<h4>Some Other Information:</h4><p>Belongs here</p>",
            "column1": "<p>A description of your beamline</p>",
            "column2": "<h4>Quicklinks</h4><ul><li>Maybe some links</li><li>To important pages</li></ul>",
            "name_short": beamline,
            "name_long": "My Beamline",
            "organization": "Our organization",
            "org_url": "https://localhost",
            "org_img": images['logo.png'],
            "background": images['pattern.png'],
            "title": "Home",
            "slug": ""
        }
        homepage = HomePage(**homeinfo)

        tag = Tag.objects.create(name="A Tag", slug="a-tag")
        catbu = PostCategory.objects.create(name="Beamline Updates", slug="beamline-updates")
        catrh = PostCategory.objects.create(name="Research Highlights", slug="research-highlights")
        catn = PostCategory.objects.create(name="News", slug="news")

        newsinfo = {
            "title": "Latest News and Developments",
            "slug": "news",
            "show_in_menus": True
        }
        newspage = NewsPage(**newsinfo)

        post1info = {
            "title": "A News Item",
            "subtitle": "This is an optional subtitle",
            "body": "<p>Here is the exciting text!</p>",
            "image": images["crystal-background.jpg"],
            "highlight": True
        }
        post2info = {
            "title": "Another News Post",
            "subtitle": "Some text",
            "body": "<p>This text is better</p>",
            "image": images["crystal-background.jpg"],
            "highlight": True,
        }
        post1 = PostPage(**post1info)
        post2 = PostPage(**post2info)

        blinfo = {
            "title": "My Beamline-1",
            "name": "My Beamline-1",
            "acronym": beamline,
            "description": "<p>A description goes here.</p>",
            "snippet": "<p>This beamline snippet is displayed on the homepage.</p>",
            "sidebar": "<h4>Techniques:</h4><ul><li>We can do almost anything</li></ul>",
            "status": "In Progress",
            "status_color": "#FF1CE5",
            "show_in_menus": True,
            "gallery": "[{\"type\": \"image\", \"value\": [{\"image\": 1, \"caption\": \"Crystals on a purple background\"}, {\"image\": 3, \"caption\": \"Honeycomb on watercolour\"}], \"id\": \"54a1ba72-c30f-439b-8b03-e7e4c1b02b40\"}]",
            "body": "[{\"type\": \"table\", \"value\": {\"data\": [[\"Row 1\", \"4\", null], [\"Row 2\", \"5\", null], [\"Total\", \"9 altogether\", null]], \"cell\": [], \"first_row_is_table_header\": false, \"first_col_is_header\": true, \"table_caption\": \"Some Specifications\"}, \"id\": \"e95cfdef-a4b2-4fd9-9293-1fd5a2042a92\"}]"
        }
        blpage = BeamlinePage(**blinfo)

        pubinfo = {
            "title": "Publications",
            "api": "https://user-portal.lightsource.ca/api/v1",
            "acronym": beamline,
            "show_in_menus": True
        }
        pubpage = PublicationsPage(**pubinfo)

        rootpage.add_child(instance=homepage)
        homepage.add_child(instance=blpage)
        homepage.add_child(instance=pubpage)
        homepage.add_child(instance=newspage)
        newspage.add_child(instance=post1)
        newspage.add_child(instance=post2)

        post1.categories.add(catbu)
        post1.tags.add(tag)
        post2.categories.add(catrh)
        post1.save()
        post2.save()

        mainsite = Site.objects.create(hostname="localhost", port=443, site_name=beamline, root_page=homepage, is_default_site=True)

        mainmenu = MainMenu.objects.create(site=mainsite, max_levels=2)

        menuitem1 = MainMenuItem.objects.create(sort_order=0, link_page=pubpage, menu=mainmenu)
        menuitem2 = MainMenuItem.objects.create(sort_order=1, link_page=blpage, menu=mainmenu)
        menuitem2 = MainMenuItem.objects.create(sort_order=2, link_page=newspage, link_text="News", menu=mainmenu)
