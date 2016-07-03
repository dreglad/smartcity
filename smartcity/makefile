all: grrah_models

grrah_models:
	python manage.py graph_models -a -g -L es -R --disable-sort-fields \
	    -X "Session,AbstractBaseSession,ModeloBase,LogEntry,recurrence.*,\
	    	 User,Group,AbstractUser,Param,Date,Rule,Recurrence,Permission,\
	    	 ContentType" \
	    -x "fecha_creacion,pk,id,fecha_modificacion" \
	    -o bd_simplificado.png
	python manage.py graph_models -a -g -L es -o bd_completo.png
