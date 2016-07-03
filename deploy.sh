# rsync to stging server (La Jornada)

rsync --dry-run -avz --exclude "*.pyc" . root@tan:/vagrant

echo 'Any key to proceed, or ctrl+c to cancel...'
read confirmation

rsync -avz --exclude "*.pyc" . root@tan:/vagrant
