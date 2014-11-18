## 1. Получить список метаданных фрагментов.

- параметры запроса:
   
   а) stream_id - целочисленный,

   b) start_time - unix time,

   c) stop_time - unix time
 
- формат запроса: 

>  http://{ip_addres}:{port}/get_meta?stream_id={stream_id}&start={start}&end={end}


- ответ в формате JSON

```
{
   "clips" : [
      {
          "clip_id": 1,
          "start": 100500,
          "stop": 100600,
          "stream_id": 2
      },
      {
          "clip_id": 2,
          "start": 200500,
          "stop": 200600,
          "stream_id": 3
      }
   ]
}
```




## 2. Получить фрагмент по идентификатору

- параметры запроса:
   
   clip_id - целочисленный
 
- формат запроса: 

>  http://{ip_addres}:{port}/get_clip/{clip_id}

- ответ: бинарные данные - массив байт фрагметна
  
