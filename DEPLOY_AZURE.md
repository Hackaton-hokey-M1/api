# 🚀 Déployer une application FastAPI sur Azure Container Instances (ACI)

## 🧩 Prérequis

* Un compte **Azure** actif
* **Azure CLI** installé
* **Docker** installé
* Une image Docker de ton application FastAPI, par exemple :

  ```
  apihockey.azurecr.io/my-image:latest
  ```
* Un **Azure Container Registry (ACR)** nommé `apihockey`

---

## 🗝️ 1. Récupérer les identifiants du registre (ACR)

Avant de déployer, récupère les identifiants du registre Azure :

```bash
15:03 $ az acr credential show --name apihockey
```

Tu obtiendras quelque chose comme :

```json
{
  "username": "apihockey",
  "passwords": [
    { "name": "password", "value": "xxxxxx" },
    { "name": "password2", "value": "yyyyyy" }
  ]
}
```

➡️ Garde ce **username** et un **password** (n’importe lequel des deux) pour la commande suivante.

---

## 🐳 2. Vérifier ou pousser ton image Docker

Assure-toi que ton image FastAPI est bien dans ton registre ACR :

```bash
az acr login --name apihockey
docker build -t apihockey.azurecr.io/my-image:latest .
docker push apihockey.azurecr.io/my-image:latest
```

---

## ⚙️ 3. (Re)Créer le conteneur dans Azure

> ⚠️ Si un conteneur du même nom existe déjà, supprime-le avant :

```bash
az container delete --name apihockey --resource-group apihockey --yes
```

Puis crée-le à nouveau :

```bash
az container create \
  --resource-group apihockey \
  --name apihockey \
  --image apihockey.azurecr.io/my-image:latest \
  --registry-login-server apihockey.azurecr.io \
  --registry-username apihockey \
  --registry-password <ton-password> \
  --ports 8000 \
  --ip-address Public \
  --os-type Linux \
  --cpu 1 \
  --memory 1.5
```

> 💡 Si tu as déjà fait `az acr login`, tu peux omettre les options `--registry-*`.

---

## 🔍 4. Vérifier le statut du conteneur

```bash
az container show \
  --resource-group apihockey \
  --name apihockey \
  --output table
```

Exemple :

```
Name         ResourceGroup    ProvisioningState    State     IpAddress
------------ ---------------- ------------------- --------- -------------
apihockey    apihockey        Succeeded            Running   20.xxx.xxx.xxx
```

---

## 🌐 5. Trouver et tester ton URL publique

Récupère ton IP :

```bash
az container show \
  --resource-group apihockey \
  --name apihockey \
  --query "{ip:ipAddress.ip}" \
  --output tsv
```

Ouvre ensuite :

```
http://<ton-ip>:8000/docs
```

---

## 🪶 6. (Optionnel) Ajouter un nom DNS fixe

Pour avoir une URL stable (qui ne change pas après redéploiement), ajoute un **nom DNS (FQDN)** :

```bash
az container create \
  --resource-group apihockey \
  --name apihockey \
  --image apihockey.azurecr.io/my-image:latest \
  --registry-login-server apihockey.azurecr.io \
  --registry-username apihockey \
  --registry-password <ton-password> \
  --ports 8000 \
  --ip-address Public \
  --dns-name-label apihockey-api \
  --os-type Linux \
  --cpu 1 \
  --memory 1.5
```

➡️ Ton API sera accessible à :

```
http://apihockey-api.francecentral.azurecontainer.io:8000/docs
```

---

## 📜 7. Vérifier les logs

```bash
az container logs \
  --resource-group apihockey \
  --name apihockey --follow
```

Tu devrais voir :

```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🧼 8. Nettoyer les ressources (optionnel)

```bash
az container delete --name apihockey --resource-group apihockey --yes
az acr delete --name apihockey --resource-group apihockey --yes
```

---

## ✅ Résumé rapide

| Étape                 | Commande clé                   | Résultat                  |
| --------------------- | ------------------------------ | ------------------------- |
| Voir identifiants ACR | `az acr credential show`       | Login + mot de passe      |
| Build image           | `docker build`                 | Image locale              |
| Push image            | `docker push`                  | Image sur ACR             |
| Créer conteneur       | `az container create`          | API déployée              |
| Voir IP               | `az container show --query ip` | URL publique              |
| Voir logs             | `az container logs`            | Vérification du démarrage |
| URL fixe              | `--dns-name-label`             | FQDN stable               |
