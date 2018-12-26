from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings

import cgi
import os


def render_pdf(url_template, contexto={}):

	template = get_template(url_template)
	html = template.render(contexto)
	result = BytesIO()


	pdf= pisa.pisaDocument(BytesIO(html.encode("UTF-8")),result,link_callback=fetch_resources)


	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type="application/pdf")
	return None


def fetch_resources(uri, rel):
	
#	path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
	sUrl = settings.STATIC_URL      # Typically /static/
	sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
	mUrl = settings.MEDIA_URL       # Typically /static/media/
	mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
	# convert URIs to absolute system paths
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))

	# make sure that file exists
	#if not os.path.isfile(path):
	#	raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
	else:
		path = uri

	return path
