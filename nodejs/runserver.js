/** 简单搭建
//引入http模块
var http = require("http");
//设置主机名
var hostName = '0.0.0.0';
//设置端口
var port = 8002;
//创建服务
var server = http.createServer(function(req,res){
    res.setHeader('Content-Type','text/plain');
    res.end("hello nodejs");

});
server.listen(port,hostName,function(){
    console.log(`Listening ${hostName}:${port}`);
});

*/

/** 进阶搭建
//安装cnpm：$ npm install -g cnpm --registry=https://registry.npm.taobao.org
//引入express ：$ cnpm install express –save
*/
var express = require("express");
var multiparty = require("multiparty");
const bodyParser = require("body-parser");
var app = express();
app.use(bodyParser.json());//数据JSON类型
app.use(bodyParser.urlencoded({ extended: false }));
var hostName = '0.0.0.0';
var port = 8080;

app.all('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1');
    res.header("Content-Type", "application/json;charset=utf-8");

    next();  
});

app.get("/get",function(req,res){
    console.log("请求url：",req.path)
    console.log("请求参数：",req.query)
    res.send("这是get请求");
})

app.post("/post",function(req,res){
    console.log("请求url：",req.path);
    console.log("请求头参数：",req.query);
    console.log("请求体参数：",req.body);
    console.log("参数a:",req.body.a);
    res.send("这是POST请求");
})

app.post('/formdata',function(req,res){
    var form = new multiparty.Form({ uploadDir: './public/images' });
    form.parse(req, function(err, fields, files) {
        console.log(fields, files,' fields2')
        if (err) {
        } else {
            //res.json({ imgSrc: files.image[0].path })
        }
    });
    res.send('formdata发送成功了');
})

app.listen(port,hostName,function(){
   console.log(`Listening ${hostName}:${port}`);
});