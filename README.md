# LSPaintboard-Django 后端说明

## 0x00 前置


在每一个服务端返回的请求中，返回值与状态码的数值相等，下表为状态码对照表

| 状态码 | `resp[0]` | url                    | status | data                |
| ------ | --------- | ---------------------- | ------ | ------------------- |
| 200    | `\x00`    | `*`                    | `200`  | `Done.`             |
| 201    | `\x01`    | `/gettoken`            | `201`  | `token`             |
| 202    | `\x02`    | /                      | /      | /                   |
| 203    | `\x03`    | `/board` / `/boardimg` | 203    | 见下                |
| 400    | `\x10`    | `*`                    | `400`  | `Token Error.`      |
| 401    | `\x11`    | `*`                    | `401`  | `Request too fast.` |
| 402    | `\x12`    | `/paint`               | `402`  | `Paint too fast.`   |
|        | `\x13`    | /                      | /      | /                   |
| 500    | `\xff`    | `*`                    | `500`  | `Server Error.`     |

## 0x01 Each

### For Everyone

+ `/board`
  请求方法：`GET`
  
  返回：以下给出 `js` 转码与 `python` 转码示例代码：
  
  ```js
  for(let i=1;i<1800001;i+=3)
  {
      y: parseInt(((i-1)/3) % 600), 
      x: parseInt(((i-1)/3)/600), 
      color: resp[i].charCodeAt(0).toString(16).padStart(2,'0') //R
          + resp[i+1].charCodeAt(0).toString(16).padStart(2,'0') //G
          + resp[i+2].charCodeAt(0).toString(16).padStart(2,'0'); //B
  }
  ```
  
  ```py
  for i in range(1, 1800001, 3):
      x: int(((i-1)/3)//600)
      y: int(((i-1)/3)%600)
      color: ((ord(board[i]),ord(board[i+1]),ord(board[i+2]))) 
  ```
  
+ `/paint`

  请求方法：`POST`

  请求体：

  ```json
  json
  {
      "x":x,  //int
      "y":y,  //int
      "token":token  //str[]
      "color":color  //str[6]
  }
  ```

  e.g. 

  ```json
  {"x":0,"y":0,"color":"FF00FF","token":"lyjsd0j1a-1701-sbsb-lyj3-042822626lyj"}
  ```

  

  返回：转 *0x00*

+ `/gettoken`

  请求方法：`GET` / `POST`
  
  请求体：
  
  ```json
  json
  {
      "uid":uid,  //int
      "paste":paste //str[8]
  }
  ```
  
  e.g. 
  
  ```json
  {"uid":710036,"paste":"d0j1albt"}
  ```
  

返回：转 *0x00*

e.g.

```
\x01lyjsd0j1a-1701-sbsb-lyj3-042822626lyj
```

+ `/boardimg`

  请求方法：`GET`
  
  返回：当前版面 PNG 文件

## For root



![](https://pbdv.uwuwu.us.kg/paintboard/boardimg)



