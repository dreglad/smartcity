all: grrah_models

grrah_models:
	python manage.py graph_models -E -S -a -L es \
	    -X "Session,AbstractBaseSession,ModeloBase,LogEntry,recurrence.*,\
	    	 User,Group,AbstractUser,Param,Date,Rule,Recurrence,Permission,\
	    	 ContentType" \
	    -x "fecha_creacion,pk,id,fecha_modificacion" \
	    -o bd_simplificado.png
	python manage.py graph_models -X "ModeloBase" -E -S -g -a -L es -o bd_completo.png

