apiVersion: v1
kind: Namespace
metadata:
  name: moon
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: moon
  namespace: moon
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: moon
  name: moon
rules:
- apiGroups:
  - ""
  resources:
  - pods
  - pods/log
  - configmaps
  - secrets
  - resourcequotas
  verbs:
  - get
  - watch
  - list
  - create
  - update
  - patch
  - delete
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: moon
  namespace: moon
roleRef:
  kind: Role
  name: moon
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  namespace: moon
  name: moon
---
#apiVersion: rbac.authorization.k8s.io/v1
#kind: RoleBinding
#metadata:
#  name: moon
#  namespace: moon
#roleRef:
#  kind: ClusterRole
#  name: edit
#  apiGroup: rbac.authorization.k8s.io
#subjects:
#- kind: ServiceAccount
#  namespace: moon
#  name: moon
#---
apiVersion: v1
kind: Service
metadata:
  name: moon
  namespace: moon
spec:
  selector:
    app: moon
  ports:
  - name: "moon"
    protocol: TCP
    port: 4444
  - name: "moon-ui"
    protocol: TCP
    port: 8080
  type: LoadBalancer
---
apiVersion: v1
kind: Service
metadata:
  name: browsers
  namespace: moon
spec:
  selector:
    moon: browser
  clusterIP: None
  publishNotReadyAddresses: true
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: moon
  namespace: moon
spec:
  replicas: 2
  selector:
    matchLabels:
      app: moon
  template:
    metadata:
      labels:
        app: moon
    spec:
      serviceAccountName: moon
      containers:
      - name: moon
        image: aerokube/moon:1.9.1
        args: ["-namespace", "moon", "-license-file", "/license/license.key", "-disable-cpu-limits", "-disable-memory-limits", "-service-account-name", "moon"]
        ports:
        - containerPort: 4444
        volumeMounts:
        - name: quota
          mountPath: /quota
          readOnly: true
        - name: config
          mountPath: /config
          readOnly: true
#        - name: credentials
#          mountPath: /credentials
#          readOnly: true
        - name: users
          mountPath: /users
          readOnly: true
        - name: license-key
          mountPath: /license
          readOnly: true
      - name: moon-api
        image: aerokube/moon-api:1.9.1
        args: ["-namespace", "moon", "-license-file", "/license/license.key", "-listen", ":8888"]
        ports:
        - containerPort: 8888
        volumeMounts:
        - name: quota
          mountPath: /quota
          readOnly: true
        - name: license-key
          mountPath: /license
          readOnly: true
      - name: selenoid-ui
        image: aerokube/selenoid-ui:1.10.3
        args: ["-status-uri", "http://localhost:8888", "-webdriver-uri", "http://localhost:4444"]
        ports:
        - name: selenoid-ui
          containerPort: 8080
      volumes:
      - name: quota
        configMap:
          name: quota
      - name: config
        configMap:
          name: config
#      - name: credentials
#        secret:
#          secretName: credentials
      - name: users
        secret:
          secretName: users
      - name: license-key
        secret:
          secretName: licensekey
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: config
  namespace: moon
data:
  service.json: |
    {
      "kernelCaps": [ "SYS_ADMIN" ]
    }
# The following is an example S3 upload configuration to be inserted to service.json above:
#
#      "s3": {
#        "endpoint": "https://storage.googleapis.com",
#        "bucketName": "moon-test",
#        "version": "S3v2"
#      }
#

  devices.json: |
    {
      "Apple iPhone 11": {
        "width": 414,
        "height": 896,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone 11 Pro": {
        "width": 375,
        "height": 812,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone 11 Pro Max": {
        "width": 414,
        "height": 896,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
      },
      "Apple iPad 10.2 (2019)": {
        "width": 810,
        "height": 1080,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
      },
      "Apple iPhone Xs": {
        "width": 375,
        "height": 812,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone Xs Max": {
        "width": 414,
        "height": 896,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone XR": {
        "width": 414,
        "height": 896,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone 5/SE": {
        "width": 320,
        "height": 568,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
      },
      "Apple iPhone 6/7/8": {
        "width": 375,
        "height": 667,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone 6/7/8 Plus": {
        "width": 414,
        "height": 736,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
      },
      "Apple iPhone X": {
        "width": 375,
        "height": 812,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
      },
      "Apple iPad": {
        "width": 768,
        "height": 1024,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
      },
      "Apple iPad Pro": {
        "width": 1024,
        "height": 1366,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
      },
      "Apple iPhone 8 Plus": {
        "width": 414,
        "height": 736,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1"
      },
      "Apple iPhone 8": {
        "width": 375,
        "height": 667,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1"
      },
      "Apple iPhone 7 Plus": {
        "width": 414,
        "height": 736,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1"
      },
      "Apple iPhone 7": {
        "width": 375,
        "height": 667,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/11.0 Mobile/14E304 Safari/604.1"
      },
      "Apple iPhone SE": {
        "width": 320,
        "height": 568,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E233 Safari/601.1"
      },
      "Apple iPad Mini 4": {
        "width": 768,
        "height": 1024,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1"
      },
      "Apple iPad Pro (10.5)": {
        "width": 834,
        "height": 1112,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B101 Safari/604.1"
      },
      "Apple iPad Pro (12.9)": {
        "width": 1024,
        "height": 1366,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B101 Safari/604.1 (KHTML, like Gecko) Chrome/66.0.3359.126 Mobile Safari/537.36"
      },
      "Apple iPad Mini": {
        "width": 768,
        "height": 1024,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
      },
      "Apple iPhone 4": {
        "width": 320,
        "height": 480,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
      },
      "Blackberry PlayBook": {
        "width": 600,
        "height": 1024,
        "pixelRatio": 1,
        "userAgent": "Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+"
      },
      "BlackBerry Z30": {
        "width": 360,
        "height": 640,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+"
      },
      "Google Nexus 4": {
        "width": 384,
        "height": 640,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Nexus 5": {
        "width": 360,
        "height": 640,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Nexus 5X": {
        "width": 412,
        "height": 732,
        "pixelRatio": 2.625,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Nexus 6": {
        "width": 412,
        "height": 732,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Nexus 6P": {
        "width": 412,
        "height": 732,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Nexus 7": {
        "width": 600,
        "height": 960,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Safari/537.36",
        "printVersion": true
      },
      "Google Nexus 10": {
        "width": 800,
        "height": 1280,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Safari/537.36",
        "printVersion": true
      },
      "Google Pixel 2": {
        "width": 411,
        "height": 731,
        "pixelRatio": 2.625,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Pixel 2 XL": {
        "width": 411,
        "height": 823,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Google Pixel 3": {
        "width": 393,
        "height": 786,
        "pixelRatio": 2.75,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36"
      },
      "Google Pixel 3 XL": {
        "width": 412,
        "height": 846,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36"
      },
      "Google Pixel 4": {
        "width": 353,
        "height": 745,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
      },
      "Google Pixel 4 XL": {
        "width": 412,
        "height": 869,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
      },
      "JioPhone 2": {
        "width": 240,
        "height": 320,
        "pixelRatio": 1,
        "userAgent": "Mozilla/5.0 (Mobile; LYF/F300B/LYF-F300B-001-01-15-130718-i;Android; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.5"
      },
      "Kindle Fire HDX": {
        "width": 800,
        "height": 1280,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true"
      },
      "Laptop with touch": {
        "width": 950,
        "height": 1280,
        "pixelRatio": 1,
        "userAgent": ""
      },
      "Laptop with HiDPI screen": {
        "width": 900,
        "height": 1440,
        "pixelRatio": 2,
        "userAgent": ""
      },
      "Laptop with MDPI screen": {
        "width": 800,
        "height": 1280,
        "pixelRatio": 1,
        "userAgent": ""
      },
      "LG Optimus L70": {
        "width": 384,
        "height": 640,
        "pixelRatio": 1.25,
        "userAgent": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Microsoft Lumia 550": {
        "width": 640,
        "height": 360,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263"
      },
      "Microsoft Lumia 950": {
        "width": 360,
        "height": 640,
        "pixelRatio": 4,
        "userAgent": "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263"
      },
      "Microsoft Surface Duo": {
        "width": 540,
        "height": 720,
        "pixelRatio": 2.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Motorola G4": {
        "width": 360,
        "height": 640,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Nokia Lumia 520": {
        "width": 320,
        "height": 533,
        "pixelRatio": 1.5,
        "userAgent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)"
      },
      "Nokia N9": {
        "width": 480,
        "height": 854,
        "pixelRatio": 1,
        "userAgent": "Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13"
      },
      "Palm PVG100": {
        "width": 360,
        "height": 640,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.1.0; PVG100 Build/OPM1.171019.019) AppleWebKit/537.36"
      },
      "Red Hydrogen One": {
        "width": 412,
        "height": 732,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.1.0; H1A1000 Build/H1A1000.010ho.01.01.01r.089) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36"
      },
      "Samsung Galaxy A20": {
        "width": 980,
        "height": 1734,
        "pixelRatio": 2.25,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36"
      },
      "Samsung Galaxy Fold": {
        "width": 586,
        "height": 820,
        "pixelRatio": 2.625,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-F900U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36"
      },
      "Samsung Galaxy Note 2": {
        "width": 360,
        "height": 640,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
      },
      "Samsung Galaxy Note 3": {
        "width": 360,
        "height": 640,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
      },
      "Samsung Galaxy Note 8": {
        "width": 412,
        "height": 846,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 7.1.1; SAMSUNG SM-N950U Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36"
      },
      "Samsung Galaxy Note 9": {
        "width": 412,
        "height": 846,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.1.0; SM-N960U Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36"
      },
      "Samsung Galaxy Note 10": {
        "width": 412,
        "height": 869,
        "pixelRatio": 2.625,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-N970XU) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36"
      },
      "Samsung Galaxy Note 10+": {
        "width": 412,
        "height": 869,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-N975XU) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/10.2 Chrome/71.0.3578.99 Mobile Safari/537.36"
      },
      "Samsung Galaxy S3": {
        "width": 360,
        "height": 640,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
      },
      "Samsung Galaxy S5": {
        "width": 360,
        "height": 640,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36",
        "printVersion": true
      },
      "Samsung Galaxy S7": {
        "width": 360,
        "height": 640,
        "pixelRatio": 4,
        "userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
      },
      "Samsung Galaxy S8": {
        "width": 360,
        "height": 740,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
      },
      "Samsung Galaxy S8+": {
        "width": 412,
        "height": 846,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 7.0; SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
      },
      "Samsung Galaxy S9": {
        "width": 360,
        "height": 740,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
      },
      "Samsung Galaxy S9+": {
        "width": 320,
        "height": 658,
        "pixelRatio": 4.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
      },
      "Samsung Galaxy S10": {
        "width": 412,
        "height": 869,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.105 Mobile Safari/537.36"
      },
      "Samsung Galaxy S10+": {
        "width": 412,
        "height": 869,
        "pixelRatio": 3.5,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.105 Mobile Safari/537.36"
      },
      "Samsung Galaxy S10e": {
        "width": 360,
        "height": 760,
        "pixelRatio": 3,
        "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.105 Mobile Safari/537.36"
      },
      "Samsung Galaxy Tab S3": {
        "width": 768,
        "height": 1024,
        "pixelRatio": 2,
        "userAgent": "Mozilla/5.0 (Linux; Android 7.0; SM-T827V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Safari/537.36"
      },
      "Samsung Galaxy Tab S4": {
        "width": 712,
        "height": 1138,
        "pixelRatio": 2.25,
        "userAgent": "Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36"
      }
    }

#---
#apiVersion: v1
#kind: Secret
#metadata:
#  name: credentials
#  namespace: moon
#stringData:
#  s3.accessKey: "access-key-value"
#  s3.secretKey: "secret-key-value"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: quota
  namespace: moon
data:
  browsers.json: |
    {
      "safari": {
        "default": "14.0",
        "versions": {
          "14.0": {
            "image": "quay.io/browsers/safari:14.0",
            "port": "4444",
            "path": "/"
          },
          "13.0": {
            "image": "quay.io/browsers/safari:13.0",
            "port": "4444",
            "path": "/"
          }
        }
      },
      "MicrosoftEdge": {
        "default": "93.0",
        "versions": {
          "93.0": {
            "image": "quay.io/browsers/edge:93.0",
            "port": "4444",
            "path": "/"
          },
          "92.0": {
            "image": "quay.io/browsers/edge:92.0",
            "port": "4444",
            "path": "/"
          },
          "91.0": {
            "image": "quay.io/browsers/edge:91.0",
            "port": "4444",
            "path": "/"
          },
          "90.0": {
            "image": "quay.io/browsers/edge:90.0",
            "port": "4444",
            "path": "/"
          },
          "89.0": {
            "image": "quay.io/browsers/edge:89.0",
            "port": "4444",
            "path": "/"
          },
          "88.0": {
            "image": "quay.io/browsers/edge:88.0",
            "port": "4444",
            "path": "/"
          }
        }
      },
      "firefox": {
        "default": "92.0",
        "versions": {
          "92.0": {
            "image": "quay.io/browsers/firefox:92.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "91.0": {
            "image": "quay.io/browsers/firefox:91.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "90.0": {
            "image": "quay.io/browsers/firefox:90.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "89.0": {
            "image": "quay.io/browsers/firefox:89.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "88.0": {
            "image": "quay.io/browsers/firefox:88.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "87.0": {
            "image": "quay.io/browsers/firefox:87.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "86.0": {
            "image": "quay.io/browsers/firefox:86.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "85.0": {
            "image": "quay.io/browsers/firefox:85.0",
            "port": "4444",
            "path": "/wd/hub"
          },
          "84.0": {
            "image": "quay.io/browsers/firefox:84.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "83.0": {
            "image": "quay.io/browsers/firefox:83.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "82.0": {
            "image": "quay.io/browsers/firefox:82.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "81.0": {
            "image": "quay.io/browsers/firefox:81.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "80.0": {
            "image": "quay.io/browsers/firefox:80.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "79.0": {
            "image": "quay.io/browsers/firefox:79.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "78.0": {
            "image": "quay.io/browsers/firefox:78.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "77.0": {
            "image": "quay.io/browsers/firefox:77.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "76.0": {
            "image": "quay.io/browsers/firefox:76.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "75.0": {
            "image": "quay.io/browsers/firefox:75.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "74.0": {
            "image": "quay.io/browsers/firefox:74.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "73.0": {
            "image": "quay.io/browsers/firefox:73.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "72.0": {
            "image": "quay.io/browsers/firefox:72.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "71.0": {
            "image": "quay.io/browsers/firefox:71.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "70.0": {
            "image": "quay.io/browsers/firefox:70.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "69.0": {
            "image": "quay.io/browsers/firefox:69.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "68.0": {
            "image": "quay.io/browsers/firefox:68.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "67.0": {
            "image": "quay.io/browsers/firefox:67.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "66.0": {
            "image": "quay.io/browsers/firefox:66.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "65.0": {
            "image": "quay.io/browsers/firefox:65.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "64.0": {
            "image": "quay.io/browsers/firefox:64.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "63.0": {
            "image": "quay.io/browsers/firefox:63.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "62.0": {
            "image": "quay.io/browsers/firefox:62.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "61.0": {
            "image": "quay.io/browsers/firefox:61.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "60.0": {
            "image": "quay.io/browsers/firefox:60.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "59.0": {
            "image": "quay.io/browsers/firefox:59.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "58.0": {
            "image": "quay.io/browsers/firefox:58.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "57.0": {
            "image": "quay.io/browsers/firefox:57.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "56.0": {
            "image": "quay.io/browsers/firefox:56.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "55.0": {
            "image": "quay.io/browsers/firefox:55.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "54.0": {
            "image": "quay.io/browsers/firefox:54.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "53.0": {
            "image": "quay.io/browsers/firefox:53.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "52.0": {
            "image": "quay.io/browsers/firefox:52.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "51.0": {
            "image": "quay.io/browsers/firefox:51.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "50.0": {
            "image": "quay.io/browsers/firefox:50.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "49.0": {
            "image": "quay.io/browsers/firefox:49.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "48.0": {
            "image": "quay.io/browsers/firefox:48.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "47.0": {
            "image": "quay.io/browsers/firefox:47.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "46.0": {
            "image": "quay.io/browsers/firefox:46.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "45.0": {
            "image": "quay.io/browsers/firefox:45.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "44.0": {
            "image": "quay.io/browsers/firefox:44.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "43.0": {
            "image": "quay.io/browsers/firefox:43.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "42.0": {
            "image": "quay.io/browsers/firefox:42.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "41.0": {
            "image": "quay.io/browsers/firefox:41.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "40.0": {
            "image": "quay.io/browsers/firefox:40.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "39.0": {
            "image": "quay.io/browsers/firefox:39.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "38.0": {
            "image": "quay.io/browsers/firefox:38.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "37.0": {
            "image": "quay.io/browsers/firefox:37.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "36.0": {
            "image": "quay.io/browsers/firefox:36.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "35.0": {
            "image": "quay.io/browsers/firefox:35.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "34.0": {
            "image": "quay.io/browsers/firefox:34.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "33.0": {
            "image": "quay.io/browsers/firefox:33.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "32.0": {
            "image": "quay.io/browsers/firefox:32.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "31.0": {
            "image": "quay.io/browsers/firefox:31.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "30.0": {
            "image": "quay.io/browsers/firefox:30.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "29.0": {
            "image": "quay.io/browsers/firefox:29.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "28.0": {
            "image": "quay.io/browsers/firefox:28.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "27.0": {
            "image": "quay.io/browsers/firefox:27.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "26.0": {
            "image": "quay.io/browsers/firefox:26.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "25.0": {
            "image": "quay.io/browsers/firefox:25.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "24.0": {
            "image": "quay.io/browsers/firefox:24.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "23.0": {
            "image": "quay.io/browsers/firefox:23.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "22.0": {
            "image": "quay.io/browsers/firefox:22.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "21.0": {
            "image": "quay.io/browsers/firefox:21.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "20.0": {
            "image": "quay.io/browsers/firefox:20.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "19.0": {
            "image": "quay.io/browsers/firefox:19.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "18.0": {
            "image": "quay.io/browsers/firefox:18.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "17.0": {
            "image": "quay.io/browsers/firefox:17.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "16.0": {
            "image": "quay.io/browsers/firefox:16.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "15.0": {
            "image": "quay.io/browsers/firefox:15.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "14.0": {
            "image": "quay.io/browsers/firefox:14.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "13.0": {
            "image": "quay.io/browsers/firefox:13.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "12.0": {
            "image": "quay.io/browsers/firefox:12.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "11.0": {
            "image": "quay.io/browsers/firefox:11.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "10.0": {
            "image": "quay.io/browsers/firefox:10.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "9.0": {
            "image": "quay.io/browsers/firefox:9.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "8.0": {
            "image": "quay.io/browsers/firefox:8.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "7.0": {
            "image": "quay.io/browsers/firefox:7.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "6.0": {
            "image": "quay.io/browsers/firefox:6.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "5.0": {
            "image": "quay.io/browsers/firefox:5.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "4.0": {
            "image": "quay.io/browsers/firefox:4.0-1",
            "port": "4444",
            "path": "/wd/hub"
          },
          "3.6": {
            "image": "quay.io/browsers/firefox:3.6-1",
            "port": "4444",
            "path": "/wd/hub"
          }
        }
      },
      "chrome": {
        "default": "93.0",
        "versions": {
          "93.0": {
            "image": "quay.io/browsers/chrome:93.0",
            "port": "4444"
          },
          "92.0": {
            "image": "quay.io/browsers/chrome:92.0",
            "port": "4444"
          },
          "91.0": {
            "image": "quay.io/browsers/chrome:91.0",
            "port": "4444"
          },
          "90.0": {
            "image": "quay.io/browsers/chrome:90.0",
            "port": "4444"
          },
          "89.0": {
            "image": "quay.io/browsers/chrome:89.0",
            "port": "4444"
          },
          "88.0": {
            "image": "quay.io/browsers/chrome:88.0-1",
            "port": "4444"
          },
          "87.0": {
            "image": "quay.io/browsers/chrome:87.0-1",
            "port": "4444"
          },
          "86.0": {
            "image": "quay.io/browsers/chrome:86.0-1",
            "port": "4444"
          },
          "85.0": {
            "image": "quay.io/browsers/chrome:85.0-1",
            "port": "4444"
          },
          "84.0": {
            "image": "quay.io/browsers/chrome:84.0-1",
            "port": "4444"
          },
          "83.0": {
            "image": "quay.io/browsers/chrome:83.0-1",
            "port": "4444"
          },
          "81.0": {
            "image": "quay.io/browsers/chrome:81.0-1",
            "port": "4444"
          },
          "80.0": {
            "image": "quay.io/browsers/chrome:80.0-1",
            "port": "4444"
          },
          "79.0": {
            "image": "quay.io/browsers/chrome:79.0-1",
            "port": "4444"
          },
          "78.0": {
            "image": "quay.io/browsers/chrome:78.0-1",
            "port": "4444"
          },
          "77.0": {
            "image": "quay.io/browsers/chrome:77.0-1",
            "port": "4444"
          },
          "76.0": {
            "image": "quay.io/browsers/chrome:76.0-1",
            "port": "4444"
          },
          "75.0": {
            "image": "quay.io/browsers/chrome:75.0-1",
            "port": "4444"
          },
          "74.0": {
            "image": "quay.io/browsers/chrome:74.0-1",
            "port": "4444"
          },
          "73.0": {
            "image": "quay.io/browsers/chrome:73.0-1",
            "port": "4444"
          },
          "72.0": {
            "image": "quay.io/browsers/chrome:72.0-1",
            "port": "4444"
          },
          "71.0": {
            "image": "quay.io/browsers/chrome:71.0-1",
            "port": "4444"
          },
          "70.0": {
            "image": "quay.io/browsers/chrome:70.0-1",
            "port": "4444"
          },
          "69.0": {
            "image": "quay.io/browsers/chrome:69.0-1",
            "port": "4444"
          },
          "68.0": {
            "image": "quay.io/browsers/chrome:68.0-1",
            "port": "4444"
          },
          "67.0": {
            "image": "quay.io/browsers/chrome:67.0-1",
            "port": "4444"
          },
          "66.0": {
            "image": "quay.io/browsers/chrome:66.0-1",
            "port": "4444"
          },
          "65.0": {
            "image": "quay.io/browsers/chrome:65.0-1",
            "port": "4444"
          },
          "64.0": {
            "image": "quay.io/browsers/chrome:64.0-1",
            "port": "4444"
          },
          "63.0": {
            "image": "quay.io/browsers/chrome:63.0-1",
            "port": "4444"
          },
          "62.0": {
            "image": "quay.io/browsers/chrome:62.0-1",
            "port": "4444"
          },
          "61.0": {
            "image": "quay.io/browsers/chrome:61.0-1",
            "port": "4444"
          },
          "60.0": {
            "image": "quay.io/browsers/chrome:60.0-1",
            "port": "4444"
          },
          "59.0": {
            "image": "quay.io/browsers/chrome:59.0",
            "port": "4444"
          },
          "58.0": {
            "image": "quay.io/browsers/chrome:58.0",
            "port": "4444"
          },
          "57.0": {
            "image": "quay.io/browsers/chrome:57.0",
            "port": "4444"
          },
          "56.0": {
            "image": "quay.io/browsers/chrome:56.0",
            "port": "4444"
          },
          "55.0": {
            "image": "quay.io/browsers/chrome:55.0",
            "port": "4444"
          },
          "54.0": {
            "image": "quay.io/browsers/chrome:54.0",
            "port": "4444"
          },
          "53.0": {
            "image": "quay.io/browsers/chrome:53.0",
            "port": "4444"
          },
          "52.0": {
            "image": "quay.io/browsers/chrome:52.0",
            "port": "4444"
          },
          "51.0": {
            "image": "quay.io/browsers/chrome:51.0",
            "port": "4444"
          },
          "50.0": {
            "image": "quay.io/browsers/chrome:50.0",
            "port": "4444"
          },
          "49.0": {
            "image": "quay.io/browsers/chrome:49.0",
            "port": "4444"
          },
          "48.0": {
            "image": "quay.io/browsers/chrome:48.0",
            "port": "4444"
          }
        }
      },
      "opera": {
        "default": "78.0",
        "versions": {
          "78.0": {
            "image": "quay.io/browsers/opera:78.0",
            "port": "4444"
          },
          "77.0": {
            "image": "quay.io/browsers/opera:77.0",
            "port": "4444"
          },
          "76.0": {
            "image": "quay.io/browsers/opera:76.0",
            "port": "4444"
          },
          "75.0": {
            "image": "quay.io/browsers/opera:75.0",
            "port": "4444"
          },
          "74.0": {
            "image": "quay.io/browsers/opera:74.0",
            "port": "4444"
          },
          "73.0": {
            "image": "quay.io/browsers/opera:73.0-1",
            "port": "4444"
          },
          "72.0": {
            "image": "quay.io/browsers/opera:72.0-1",
            "port": "4444"
          },
          "71.0": {
            "image": "quay.io/browsers/opera:71.0-1",
            "port": "4444"
          },
          "70.0": {
            "image": "quay.io/browsers/opera:70.0-1",
            "port": "4444"
          },
          "69.0": {
            "image": "quay.io/browsers/opera:69.0-1",
            "port": "4444"
          },
          "68.0": {
            "image": "quay.io/browsers/opera:68.0-1",
            "port": "4444"
          },
          "67.0": {
            "image": "quay.io/browsers/opera:67.0-1",
            "port": "4444"
          },
          "66.0": {
            "image": "quay.io/browsers/opera:66.0-1",
            "port": "4444"
          },
          "65.0": {
            "image": "quay.io/browsers/opera:65.0-1",
            "port": "4444"
          },
          "64.0": {
            "image": "quay.io/browsers/opera:64.0-1",
            "port": "4444"
          },
          "63.0": {
            "image": "quay.io/browsers/opera:63.0-1",
            "port": "4444"
          },
          "62.0": {
            "image": "quay.io/browsers/opera:62.0",
            "port": "4444"
          },
          "60.0": {
            "image": "quay.io/browsers/opera:60.0",
            "port": "4444"
          },
          "58.0": {
            "image": "quay.io/browsers/opera:58.0",
            "port": "4444"
          },
          "57.0": {
            "image": "quay.io/browsers/opera:57.0",
            "port": "4444"
          },
          "56.0": {
            "image": "quay.io/browsers/opera:56.0",
            "port": "4444"
          },
          "55.0": {
            "image": "quay.io/browsers/opera:55.0",
            "port": "4444"
          },
          "54.0": {
            "image": "quay.io/browsers/opera:54.0",
            "port": "4444"
          },
          "53.0": {
            "image": "quay.io/browsers/opera:53.0",
            "port": "4444"
          },
          "52.0": {
            "image": "quay.io/browsers/opera:52.0",
            "port": "4444"
          },
          "51.0": {
            "image": "quay.io/browsers/opera:51.0",
            "port": "4444"
          },
          "50.0": {
            "image": "quay.io/browsers/opera:50.0",
            "port": "4444"
          },
          "49.0": {
            "image": "quay.io/browsers/opera:49.0",
            "port": "4444"
          },
          "48.0": {
            "image": "quay.io/browsers/opera:48.0",
            "port": "4444"
          },
          "47.0": {
            "image": "quay.io/browsers/opera:47.0",
            "port": "4444"
          },
          "46.0": {
            "image": "quay.io/browsers/opera:46.0",
            "port": "4444"
          },
          "45.0": {
            "image": "quay.io/browsers/opera:45.0",
            "port": "4444"
          },
          "44.0": {
            "image": "quay.io/browsers/opera:44.0",
            "port": "4444"
          },
          "43.0": {
            "image": "quay.io/browsers/opera:43.0",
            "port": "4444"
          },
          "42.0": {
            "image": "quay.io/browsers/opera:42.0",
            "port": "4444"
          },
          "41.0": {
            "image": "quay.io/browsers/opera:41.0",
            "port": "4444"
          },
          "40.0": {
            "image": "quay.io/browsers/opera:40.0",
            "port": "4444"
          },
          "39.0": {
            "image": "quay.io/browsers/opera:39.0",
            "port": "4444"
          },
          "38.0": {
            "image": "quay.io/browsers/opera:38.0",
            "port": "4444"
          },
          "37.0": {
            "image": "quay.io/browsers/opera:37.0",
            "port": "4444"
          },
          "36.0": {
            "image": "quay.io/browsers/opera:36.0",
            "port": "4444"
          },
          "35.0": {
            "image": "quay.io/browsers/opera:35.0",
            "port": "4444"
          },
          "34.0": {
            "image": "quay.io/browsers/opera:34.0",
            "port": "4444"
          },
          "33.0": {
            "image": "quay.io/browsers/opera:33.0",
            "port": "4444"
          },
          "12.16": {
            "image": "quay.io/browsers/opera:12.16-1",
            "port": "4444",
            "path": "/wd/hub"
          }
        }
      }
    }
---
apiVersion: v1
kind: Secret
metadata:
  name: users
  namespace: moon
stringData:
  users.htpasswd: ""
---
apiVersion: v1
kind: Secret
metadata:
  name: licensekey
  namespace: moon
stringData:
  license.key: MG1RSVdpc2Z6YjdQQVZjd2lpei9KMkd1T3dzMTFuL1dlRjVSc3NOMUcxZk9QaUxWa3Q5SnBIakIxa09wWm0vVFJqQ0tsa21xVG1OODVRZnlQbjBjVmRHVWFLampTOFF1a3VLRXRPcEUwbnEySG16QWFQWHRDYTVjMm9jZzZFaUJqeFd5ODE4UFBHZzNCNWpCYXlha3oweFBscFl1RnB0V0U1Q3FwOGl5VDdKTk9abG5aSmlPdnRmZDFvSG1nNnVwVXBLV2E4RmYwWHcreERIR29ZTE1XTldPb1hvT2ZCUnZpcDhPWW05a1FqN0hBWWVOYUtLT1lPWlVJa1dsb1gxdjNOT1htTFpZalhsQ3h1Q3V6NWhiQjIwSjVIY0JTYnZybm9zYm14RXFkSFpQWVBKWUlKTzZvVlBnODhQeFErZ1EyTk5sWG82TC9XeXU3aisrNU0rSEdPcXlOSEdlNGx4Zm1nNVhjMWlnNkN1OCtNSVVYRzNqUllqOUY4ZHdReWpSbFNMNmFpL2dRQnc3TzY0U0lwdVF2d29jYi9kVzFSYWFRVkd3ZXYrOVdING8zRWRrYkVONUhRTmQ2MUxsUnFNdmtKeWVHV21tVlVUZ2dsMDRsTFFLTmZNVG81L2JVakNBMGhNeER5VHNJdmVRRGFMMklvTWpvcFk4VERlK1U2bUJvUDVxNVYrcCtDQVhjbjYxQlRaUVp0bmNqL0JBVkdNOEZ4NW9rWHRYSVAxUkY0a1VCckZVTDFyTWF1VkZqSk5xU1pLT293dUpMTTg2SEZ0Sld0eUlRK3ZZZm1pZU0xM292MnVleDBoRlhRdFkvMkt1dUhhN3dKV2pFT0pqaEVzTjhXSy82ZlFFbi9EQzcrNkw3NzhlbmVVZ2lLZ3VFbjlMMXZMYVZ5VWtQaWc9O2V5SnNhV05sYm5ObFpTSTZJa1JsWm1GMWJIUWlMQ0p3Y205a2RXTjBJam9pVFc5dmJpSXNJbTFoZUZObGMzTnBiMjV6SWpvMGZRPT0=


Export arc(patch.py) to datalncloud
