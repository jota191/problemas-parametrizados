from django.shortcuts import render, redirect, HttpResponse
from os import listdir
from os.path import isfile, join
import pdb
import os
import shutil

from param.parametrizar import parametrizar_eval, parsear_ejercicio

def evaluaciones(request):
	dir_ejes = 'ejercicios'

	if request.method == "GET":
		preview = request.GET.get("preview", None)
		descargar = request.GET.get("descargar", None)
		if preview:
			nombre = parametrizar_eval('Vista Previa Ejercicio', [preview], 1, False, True, False)
			response = HttpResponse(open(join(nombre, '1.pdf'), 'rb').read(), content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename=preview.pdf'
			shutil.rmtree(nombre)
			return response
		if descargar:
			response = HttpResponse(open(descargar, 'rb').read(), content_type='application/force-download')
			response['Content-Disposition'] = 'inline; filename=' + descargar.split('/')[-1]
			return response

		else:

			ejercicios = [join('ejercicios', e) for e in listdir('ejercicios') if isfile(join('ejercicios', e)) and e[-4:] == '.txt'] # if has less than 4 characters will break
			ejercicios_parseados = [parsear_ejercicio(e) for e in ejercicios]
			# pdb.set_trace()
			return render(request, 'evaluaciones.html', {'ejercicios': ejercicios_parseados, 'cantidades': range(1, 501)})


	else:
		titulo = request.POST.get("titulo", None)
		exportacion = request.POST.get("exportacion", None)
		cantidad = int(request.POST.get("cantidad", None))
		ejercicios = request.POST.getlist("ejercicios", None)
		# pdb.set_trace()
		nombre = parametrizar_eval(
			titulo,
			ejercicios,
			cantidad,
			exportacion == 'txt',
			exportacion == 'pdf', 
			exportacion == 'eva')

		if exportacion == 'txt' or exportacion == 'pdf':
			shutil.make_archive(nombre, 'zip', nombre)
			zippeado = nombre + '.zip'
			response = HttpResponse(open(zippeado, 'rb').read(), content_type='application/force-download')
			response['Content-Disposition'] = 'inline; filename=' + zippeado
			os.remove(zippeado)
			shutil.rmtree(nombre)
			return response

		if exportacion == 'eva':
			response = HttpResponse(open(nombre, 'rb').read(), content_type='application/force-download')
			response['Content-Disposition'] = 'inline; filename=' + nombre
			os.remove(nombre)
			return response

		return render(request, 'evaluaciones.html')