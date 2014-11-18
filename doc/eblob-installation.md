#### 1) Добавить в файл /etc/apt/sources.list строчку


```bash
deb http://repo.reverbrain.com/trusty/ current/amd64/
```

или для 32х разрядной архитектуры:

```bash
deb http://repo.reverbrain.com/trusty/ current/source/
```



#### 2) выполнить комманды:


```bash
sudo apt-get update

sudo apt-get install eblob
```



#### 3) в конфигурации хранилища установить путь к питоновским биндингам:


```python
LIBEBLOB_PATH = '/usr/lib64/'
```

или для 32х разрядной архитектуры:

```python
LIBEBLOB_PATH = '/usr/lib/'
```

