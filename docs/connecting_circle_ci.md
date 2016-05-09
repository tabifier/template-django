# Connecting CircleCI to Google's Docker Registry

We need to use the JSON Key file to authenticate docker login. To use this
approach, you need to create a service account JSON key file is a long-lived
credential that is scoped to a specific Cloud Platform Console project and its
resources.

* Create one [here](https://support.google.com/cloud/answer/6158849#serviceaccounts])
  and download the JSON file and note the email address created.

* Go to the [permissions](https://console.developers.google.com/permissions/projectpermissions)
  section and remove the editor access for the newly created service account.

* Go to [Google Storage](https://console.developers.google.com/storage/browser)
  and add a "**User**" permission with "**WRITE**" access with the email address
  created in the first step.

* Place the JSON file as an environment variable and use the following to login
  to Docker 

  ```bash
  docker login -e <EMAIL_ADDRESS> -u _json_key -p "$GCR_JSON_KEY" https://gcr.io
  ```

### References
 * https://circleci.com/docs/docker
 * https://cloud.google.com/container-registry/docs/auth
 * https://cloud.google.com/storage/docs/access-control?hl=en#applyacls
