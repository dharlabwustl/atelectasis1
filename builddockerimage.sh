./bashtowriteDockerfile.sh
echo "  "
command=""
for x in *.json ;
do 
	command="${command}   ${x}  "
done
echo $command
python /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/FROM_DOCUMENTS/docker-images/command2label.py  $command  >> ./Dockerfile
 imagename=$1

docker build -t sharmaatul11/${imagename} . 
#docker push sharmaatul11/${imagename}
