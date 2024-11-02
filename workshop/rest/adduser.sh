source ../../.env
JSON_DATA=`cat johndoe.json`
BEARER_TOKEN=`cat token`
echo $JSON_DATA
echo $BEARER_TOKEN

curl -L -X GET "https://key.lesgrandsvoisins.com/admin/realms/master/users/count?username=list" \
-H "Authorization: Bearer $BEARER_TOKEN" \
-H 'Content-Type: application/json'

# curl -L -X POST "https://key.lesgrandsvoisins.com/admin/realms/master/users"   \
# -H "accept: */*" \
# -H "Authorization: Bearer ${BEARER_TOKEN}"  \
# -H "Content-Type: application/json" \
# -d $JSON_DATA