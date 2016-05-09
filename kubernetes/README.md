## Tips

### Port Forwarding
You can forward the port of any Kubernetes pod with the following command:

```bash
kubectl port-forward <POD_NAME> <LOCAL_PORT>:<REMOTE_PORT>
```
Example:
```bash
kubectl port-forward elasticsearch 5000:9200
```
then you can point your browser to http://localhost:5000

**Reference:** http://kubernetes.io/docs/user-guide/connecting-to-applications-port-forward/
