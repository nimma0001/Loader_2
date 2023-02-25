api[0]="2ac76e88-259e-4c90-9088-90e6cfac3558"
api[1]="a68c2591-19f6-417a-96f6-a7db4a8afa93"
api[2]="99259056-1bf8-46a7-a595-d875f640f281"
api[3]="c9441fe7-31f1-4257-b7a9-62a4fd55d3d8"
api[4]="8e312a99-f6af-4e4d-bd43-04721db3fb61"
api[5]="5e6b4c02-09a7-4736-9c75-27dd6855c9e4"
api[6]="2dc2c4f1-671c-426e-b01b-735c3b3f6a06"
rand=$[$RANDOM % ${#api[@]}]
echo "$1 uploading pixel"; \
curl -g https://pixeldrain.com/api/file/ -u:${api[$rand]} --upload-file "$1"; \
echo "$1 uploaded pixel drain"; \
echo "$1 UPLOADING onedrive"; \
rclone copy "$1" one:Public/2023/Feb/"$3"; \
echo "$1 uploaded onedrive"; \
echo "script complete"
