## Creating Google Cloud Persistent Volumes

* Create the volume https://console.cloud.google.com/compute/disks

* Attach it to any instance and format it
  ```bash
  $ sudo mkfs.ext4 -F DISK_LOCATION  
  ```
  **Example:**
  ```bash
  $ sudo mkfs.ext4 -F /dev/sdb  
  ```
  **References:**
  *  [Attaching a disk to an existing instance](https://cloud.google.com/compute/docs/disks/persistent-disks#attachdiskrunninginstance)
  * [Formatting the instance](https://cloud.google.com/compute/docs/disks/persistent-disks#formatting)


* Detach the volume from the instance and create a Kubernetes Persistent Volume
  ```bash
  $ kubernetes create -f persistent-volume-pv001.yml
  ```
  **Reference:**
  * [Kubernetes Persistent Volumes](http://kubernetes.io/docs/user-guide/persistent-volumes/#provisioning)
  * [Kubernetes File Objects API](https://htmlpreview.github.io/?https://github.com/kubernetes/kubernetes/release-1.1/docs/api-reference/v1/definitions.html#_v1_podlist)


* Create a PersistentVolumeClaim (PVC)
  ```bash
  $ kubernetes create -f persistent-volume-claim-elastic.yml
  ```

* You can now start using the PVC as in `elasticsearch.yml`.


## Running Elastic Search in a cluster

  * As the demand for search grows, we'll need to consider clustering elastic search

    **Reference: ** https://github.com/roller-io/elasticsearch-cloud-kubernetes
