source ../../.env


curl --location --request POST 'http://key.lesgrandsvoisins.com/auth/realms/master/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode "client_id=${OICD_NAME}" \
--data-urlencode "client_secret=${OICD_SECRET}"-

# JSON_DATA = `cat john_doe.json`
# curl -i -X POST \
# https://key.lesgrandsvoisins.com/admin/realms/master/users \
# -H "accept: */*" \
# -H "Authorization: Bearer eyJhbGciOiJ...."  \
# -H "Content-Type: application/json" \
# -d $JSON_DATA