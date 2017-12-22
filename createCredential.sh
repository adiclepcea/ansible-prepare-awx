#! /bin/bash
tower-cli credential create --name="RPI Credential" --organization=RPIOrg --credential-type=Machine --inputs="`printf \"username: pi \nssh_key_data: | \n  $(sed ':a;N;$!ba;s/\n/\n  /g' keys/awx)\"`" -u admin -p password -h https://localhost --insecure
