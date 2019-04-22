#!/bin/bash

i# any future command that fails will exit the script
set -e

#  write the public key of our aws instance
eval $(ssh-agent -s)
echo "$PRIVATE_KEY" | tr -d '\r' | ssh-add - > /dev/null

# disable host key checking
./deploy/disableHostKeyChecking.sh

# use DEPLOY_SERVERS in gitlab settings
DEPLOY_SERVERS=$DEPLOY_SERVERS

# lets split this string and convert this into array
# In UNIX, we can use this commond to do this
# ${string//substring/replacement}
# our substring is "," and we replace it with nothing.
ALL_SERVERS=(${DEPLOY_SERVERS//,/ })
echo "ALL_SERVERS ${ALL_SERVERS}"

# Lets iterate over this array and ssh into each EC2 instance
# Once inside the server, run updateAndRestart.sh
for server in "${ALL_SERVERS[@]}"
do
  echo "deploying to ${server}"
  ssh ec2-user@${server} 'bash' < ./deploy/updateAndRestart.sh
done

