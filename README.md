# Leeds Schools Cultural Engagement



## Deployment

### Live

The live site is visible at <https://culturallearningleeds.com/>

A deno task has been created to deploy to the server. This requires the sshpass and rsync commands to be installed.

The two following environment variables need to be set:

* `SSHHOST` Host for the deployment
* `SSHUSER` User for the deployment
* `SSHPASS` Password for the deployment

This is automated via the [deploy-via-ssh.yml](.github/workflows/deploy-via-ssh.yml) action.
The environment variables listed above are passed in as
[Repository secrets](https://github.com/open-innovations/leeds-schools-cultural-engagement/settings/secrets/actions).

### Dev

Dev branch deplopys to github pages.

To make this work the **github-pages** environment needs to be altered to accept deployments from a different branch other than `main`.

https://github.com/open-innovations/leeds-schools-cultural-engagement/settings/environments

If the site is built with the DENO_ENV=dev variable set (e.g. DENO_ENV=dev deno task serve),
the `build.env` variable will be set to dev, which adds the `dev_banner` component just under the header.