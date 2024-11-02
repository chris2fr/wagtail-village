  source ../../.env
  echo "Client ${OPENID_NAME}"
  curl -L -X POST "https://key.lesgrandsvoisins.com/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=admin-cli" \
  --data-urlencode "grant_type=password" \
  --data-urlencode 'username=newuser' \
  --data-urlencode "password=$NEWUSER_PASSWORD" | 
  python -m json.tool
