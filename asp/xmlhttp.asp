<%
'GET方法
Function GetHttpPage(HttpUrl)
If IsNull(HttpUrl)=True Or Len(HttpUrl)<18 Or HttpUrl="$False$" Then
GetHttpPage="$False$"
Exit Function
End If
Dim Http
Set Http=server.createobject("MSXML2.XMLHTTP")
Http.open "GET",HttpUrl,False
Http.Send()
If Http.Readystate<>4 then
Set Http=Nothing 
GetHttpPage="$False$"
Exit function
End if
GetHTTPPage=bytesToBSTR(Http.responseBody,"GB2312")
Set Http=Nothing
If Err.number<>0 then
Err.Clear
End If
End Function

'类型转换
Function BytesToBstr(Body,Cset)
Dim Objstream
Set Objstream = Server.CreateObject("adodb.stream")
objstream.Type = 1
objstream.Mode =3
objstream.Open
objstream.Write body
objstream.Position = 0
objstream.Type = 2
objstream.Charset = Cset
BytesToBstr = objstream.ReadText 
objstream.Close
set objstream = nothing
End Function
   
 
'POST方法
Function PostHttpPage(RefererUrl,PostUrl,PostData) 
Dim xmlHttp 
Dim RetStr 
Set xmlHttp = CreateObject("Msxml2.XMLHTTP") 
'Set xmlHttp = CreateObject("WinHTTP.WinHTTPRequest.5.1")
xmlHttp.Open "POST", PostUrl, true
XmlHTTP.setRequestHeader "Content-Length",Len(PostData) 
xmlHttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"
xmlHttp.setRequestHeader "Referer", RefererUrl
xmlHttp.Send PostData 
If Err.Number <> 0 Then 
Set xmlHttp=Nothing
PostHttpPage = "$False$"
Exit Function
End If
'PostHttpPage=bytesToBSTR(xmlHttp.responseBody,"GB2312")
Set xmlHttp = nothing
End Function

'编码转换
Function UrlEncoding(DataStr)
Dim StrReturn,Si,ThisChr,InnerCode,Hight8,Low8
StrReturn = ""
For Si = 1 To Len(DataStr)
ThisChr = Mid(DataStr,Si,1)
If Abs(Asc(ThisChr)) < &HFF Then
StrReturn = StrReturn & ThisChr
Else
InnerCode = Asc(ThisChr)
If InnerCode < 0 Then
InnerCode = InnerCode + &H10000
End If
Hight8 = (InnerCode And &HFF00)\ &HFF
Low8 = InnerCode And &HFF
StrReturn = StrReturn & "%" & Hex(Hight8) & "%" & Hex(Low8)
End If
Next
UrlEncoding = StrReturn
End Function

'函数名：GetBody
'作 用：截取字符串
'参 数：ConStr ------将要截取的字符串
'参 数：StartStr ------开始字符串
'参 数：OverStr ------结束字符串
'参 数：IncluL ------是否包含StartStr
'参 数：IncluR ------是否包含OverStr
'==================================================
Function GetBody(ConStr,StartStr,OverStr,IncluL,IncluR)
If ConStr="$False$" or ConStr="" or IsNull(ConStr)=True Or StartStr="" or IsNull(StartStr)=True Or OverStr="" or IsNull(OverStr)=True Then
GetBody="$False$"
Exit Function
End If
Dim ConStrTemp
Dim Start,Over
ConStrTemp=Lcase(ConStr)
StartStr=Lcase(StartStr)
OverStr=Lcase(OverStr)
Start = InStrB(1, ConStrTemp, StartStr, vbBinaryCompare)
If Start<=0 then
GetBody="$False$"
Exit Function
Else
If IncluL=False Then
Start=Start+LenB(StartStr)
End If
End If
Over=InStrB(Start,ConStrTemp,OverStr,vbBinaryCompare)
If Over<=0 Or Over<=Start then
GetBody="$False$"
Exit Function
Else
If IncluR=True Then
Over=Over+LenB(OverStr)
End If
End If
GetBody=MidB(ConStr,Start,Over-Start)
End Function
						 
'函数名：GetArray
'作 用：提取链接地址，以$Array$分隔
'参 数：ConStr ------提取地址的原字符
'参 数：StartStr ------开始字符串
'参 数：OverStr ------结束字符串
'参 数：IncluL ------是否包含StartStr
'参 数：IncluR ------是否包含OverStr
'==================================================
Function GetArray(Byval ConStr,StartStr,OverStr,IncluL,IncluR)
If ConStr="$False$" or ConStr="" Or IsNull(ConStr)=True or StartStr="" Or OverStr="" or IsNull(StartStr)=True Or IsNull(OverStr)=True Then
GetArray="$False$"
Exit Function
End If
Dim TempStr,TempStr2,objRegExp,Matches,Match
TempStr=""
Set objRegExp = New Regexp 
objRegExp.IgnoreCase = True 
objRegExp.Global = True
objRegExp.Pattern = "("&StartStr&").+?("&OverStr&")"
Set Matches =objRegExp.Execute(ConStr) 
For Each Match in Matches
TempStr=TempStr & "$Array$" & Match.Value
Next 
Set Matches=nothing

If TempStr="" Then
GetArray="$False$"
Exit Function
End If
TempStr=Right(TempStr,Len(TempStr)-7)
If IncluL=False then
objRegExp.Pattern =StartStr
TempStr=objRegExp.Replace(TempStr,"")
End if
If IncluR=False then
objRegExp.Pattern =OverStr
TempStr=objRegExp.Replace(TempStr,"")
End if
Set objRegExp=nothing

TempStr=Replace(TempStr,"""","")
TempStr=Replace(TempStr,"'","")
TempStr=Replace(TempStr," ","")
If TempStr="" then
GetArray="$False$"
Else
GetArray=TempStr
End if
End Function

'函数名：DefiniteUrl
'作 用：将相对地址转换为绝对地址
'参 数：PrimitiveUrl ------要转换的相对地址
'参 数：ConsultUrl ------当前网页地址
'==================================================
Function DefiniteUrl(Byval PrimitiveUrl,Byval ConsultUrl)
Dim ConTemp,PriTemp,Pi,Ci,PriArray,ConArray
If PrimitiveUrl="" or ConsultUrl="" or PrimitiveUrl="$False$" or ConsultUrl="$False$" Then
DefiniteUrl="$False$"
Exit Function
End If
If Left(Lcase(ConsultUrl),7)<>"http://" Then
ConsultUrl= "http://" & ConsultUrl
End If
ConsultUrl=Replace(ConsultUrl,"\","/")
ConsultUrl=Replace(ConsultUrl,"://",":\\")
PrimitiveUrl=Replace(PrimitiveUrl,"\","/")

If Right(ConsultUrl,1)<>"/" Then
If Instr(ConsultUrl,"/")>0 Then
If Instr(Right(ConsultUrl,Len(ConsultUrl)-InstrRev(ConsultUrl,"/")),".")>0 then 
Else
ConsultUrl=ConsultUrl & "/"
End If
Else
ConsultUrl=ConsultUrl & "/"
End If
End If
ConArray=Split(ConsultUrl,"/")

If Left(LCase(PrimitiveUrl),7) = "http://" then
DefiniteUrl=Replace(PrimitiveUrl,"://",":\\")
ElseIf Left(PrimitiveUrl,1) = "/" Then
DefiniteUrl=ConArray(0) & PrimitiveUrl
ElseIf Left(PrimitiveUrl,2)="./" Then
PrimitiveUrl=Right(PrimitiveUrl,Len(PrimitiveUrl)-2)
If Right(ConsultUrl,1)="/" Then 
DefiniteUrl=ConsultUrl & PrimitiveUrl
Else
DefiniteUrl=Left(ConsultUrl,InstrRev(ConsultUrl,"/")) & PrimitiveUrl
End If
ElseIf Left(PrimitiveUrl,3)="../" then
Do While Left(PrimitiveUrl,3)="../"
PrimitiveUrl=Right(PrimitiveUrl,Len(PrimitiveUrl)-3)
Pi=Pi+1
Loop 
For Ci=0 to (Ubound(ConArray)-1-Pi)
If DefiniteUrl<>"" Then
DefiniteUrl=DefiniteUrl & "/" & ConArray(Ci)
Else
DefiniteUrl=ConArray(Ci)
End If
Next
DefiniteUrl=DefiniteUrl & "/" & PrimitiveUrl
Else
If Instr(PrimitiveUrl,"/")>0 Then
PriArray=Split(PrimitiveUrl,"/")
If Instr(PriArray(0),".")>0 Then
If Right(PrimitiveUrl,1)="/" Then
DefiniteUrl="http:\\" & PrimitiveUrl
Else
If Instr(PriArray(Ubound(PriArray)-1),".")>0 Then 
DefiniteUrl="http:\\" & PrimitiveUrl
Else
DefiniteUrl="http:\\" & PrimitiveUrl & "/"
End If
End If 
Else
If Right(ConsultUrl,1)="/" Then 
DefiniteUrl=ConsultUrl & PrimitiveUrl
Else
DefiniteUrl=Left(ConsultUrl,InstrRev(ConsultUrl,"/")) & PrimitiveUrl
End If
End If
Else
If Instr(PrimitiveUrl,".")>0 Then
If Right(ConsultUrl,1)="/" Then
If right(LCase(PrimitiveUrl),3)=".cn" or right(LCase(PrimitiveUrl),3)="com" or right(LCase(PrimitiveUrl),3)="net" or right(LCase(PrimitiveUrl),3)="org" Then
DefiniteUrl="http:\\" & PrimitiveUrl & "/"
Else
DefiniteUrl=ConsultUrl & PrimitiveUrl
End If
Else
If right(LCase(PrimitiveUrl),3)=".cn" or right(LCase(PrimitiveUrl),3)="com" or right(LCase(PrimitiveUrl),3)="net" or right(LCase(PrimitiveUrl),3)="org" Then
DefiniteUrl="http:\\" & PrimitiveUrl & "/"
Else
DefiniteUrl=Left(ConsultUrl,InstrRev(ConsultUrl,"/")) & "/" & PrimitiveUrl
End If
End If
Else
If Right(ConsultUrl,1)="/" Then
DefiniteUrl=ConsultUrl & PrimitiveUrl & "/"
Else
DefiniteUrl=Left(ConsultUrl,InstrRev(ConsultUrl,"/")) & "/" & PrimitiveUrl & "/"
End If 
End If
End If
End If
If Left(DefiniteUrl,1)="/" then
DefiniteUrl=Right(DefiniteUrl,Len(DefiniteUrl)-1)
End if
If DefiniteUrl<>"" Then
DefiniteUrl=Replace(DefiniteUrl,"//","/")
DefiniteUrl=Replace(DefiniteUrl,":\\","://")
Else
DefiniteUrl="$False$"
End If
End Function
	
'函数名：ReplaceSaveRemoteFile
'作 用：替换、保存远程图片
'参 数：ConStr ------ 要替换的字符串
'参 数：SaveTf ------ 是否保存文件，False不保存，True保存
'参 数: TistUrl------ 当前网页地址
'==================================================
Function ReplaceSaveRemoteFile(ConStr,strInstallDir,strChannelDir,SaveTf,TistUrl)
If ConStr="$False$" or ConStr="" or strInstallDir="" or strChannelDir="" Then
ReplaceSaveRemoteFile=ConStr
Exit Function
End If
Dim TempStr,TempStr2,TempStr3,Re,Matches,Match,Tempi,TempArray,TempArray2
Dim Start1,Start2

Set Re = New Regexp 
Re.IgnoreCase = True 
Re.Global = True
Re.Pattern ="<img.+?[^\>]>"
Set Matches =Re.Execute(ConStr) 
For Each Match in Matches
If TempStr<>"" then 
TempStr=TempStr & "$Array$" & Match.Value
Else
TempStr=Match.Value
End if
Next
If TempStr<>"" Then
TempArray=Split(TempStr,"$Array$")
TempStr=""
For Tempi=0 To Ubound(TempArray)
Re.Pattern ="src\s*=\s*.+?\.(gif|jpg|bmp|jpeg|psd|png|svg|dxf|wmf|tiff)"
Set Matches =Re.Execute(TempArray(Tempi)) 
For Each Match in Matches
If TempStr<>"" then 
TempStr=TempStr & "$Array$" & Match.Value
Else
TempStr=Match.Value
End if
Next
Next
End if
If TempStr<>"" Then
Re.Pattern ="src\s*=\s*"
TempStr=Re.Replace(TempStr,"")
End If
Set Matches=nothing
Set Re=nothing
If TempStr="" or IsNull(TempStr)=True Then
ReplaceSaveRemoteFile=ConStr
Exit function
End if
TempStr=Replace(TempStr,"""","")
TempStr=Replace(TempStr,"'","")
TempStr=Replace(TempStr," ","")

Dim RemoteFileurl,SavePath,PathTemp,DtNow,strFileName,strFileType,ArrSaveFileName,RanNum,Arr_Path
DtNow=Now()
If SaveTf=True then
SavePath=strInstallDir & strChannelDir & "/UploadFiles/" & year(DtNow) & right("0" & month(DtNow),2) & "/"
Arr_Path=Split(SavePath,"/")
PathTemp=""
For Tempi=0 To Ubound(Arr_Path)
If Tempi=0 Then
PathTemp=Arr_Path(0) & "/"
ElseIf Tempi=Ubound(Arr_Path) Then
Exit For
Else
PathTemp=PathTemp & Arr_Path(Tempi) & "/"
End If
If CheckDir(PathTemp)=False Then
If MakeNewsDir(PathTemp)=False Then
SaveTf=False
Exit For
End If
End If
Next
End If

'去掉重复图片开始
TempArray=Split(TempStr,"$Array$")
TempStr=""
For Tempi=0 To Ubound(TempArray)
If Instr(Lcase(TempStr),Lcase(TempArray(Tempi)))<1 Then
TempStr=TempStr & "$Array$" & TempArray(Tempi)
End If
Next
TempStr=Right(TempStr,Len(TempStr)-7)
TempArray=Split(TempStr,"$Array$")
'去掉重复图片结束

'转换相对图片地址开始
TempStr=""
For Tempi=0 To Ubound(TempArray)
TempStr=TempStr & "$Array$" & DefiniteUrl(TempArray(Tempi),TistUrl)
Next
TempStr=Right(TempStr,Len(TempStr)-7)
TempStr=Replace(TempStr,Chr(0),"")
TempArray2=Split(TempStr,"$Array$")
TempStr=""
'转换相对图片地址结束

'图片替换/保存
Set Re = New Regexp
Re.IgnoreCase = True 
Re.Global = True

For Tempi=0 To Ubound(TempArray2)
RemoteFileUrl=TempArray2(Tempi)
If RemoteFileUrl<>"$False$" And SaveTf=True Then'保存图片
ArrSaveFileName = Split(RemoteFileurl,".")
   strFileType=Lcase(ArrSaveFileName(Ubound(ArrSaveFileName)))'文件类型
If strFileType="asp" or strFileType="asa" or strFileType="aspx" or strFileType="cer" or strFileType="cdx" or strFileType="exe" or strFileType="rar" or strFileType="zip" then
UploadFiles=""
ReplaceSaveRemoteFile=ConStr
Exit Function
End If

Randomize
RanNum=Int(900*Rnd)+100
   strFileName = year(DtNow) & right("0" & month(DtNow),2) & right("0" & day(DtNow),2) & right("0" & hour(DtNow),2) & right("0" & minute(DtNow),2) & right("0" & second(DtNow),2) & ranNum & "." & strFileType
Re.Pattern =TempArray(Tempi)
   If SaveRemoteFile(SavePath & strFileName,RemoteFileUrl)=True Then
PathTemp=Replace(SavePath &strFileName,strInstallDir & strChannelDir & "/","[InstallDir_ChannelDir]")
ConStr=Re.Replace(ConStr,PathTemp)
Re.Pattern=strInstallDir & strChannelDir & "/"
UploadFiles=UploadFiles & "|" & Re.Replace(SavePath &strFileName,"")
Else
PathTemp=RemoteFileUrl
ConStr=Re.Replace(ConStr,PathTemp)
'UploadFiles=UploadFiles & "|" & RemoteFileUrl
End If
ElseIf RemoteFileurl<>"$False$" and SaveTf=False Then'不保存图片
Re.Pattern =TempArray(Tempi)
ConStr=Re.Replace(ConStr,RemoteFileUrl)
UploadFiles=UploadFiles & "|" & RemoteFileUrl
End If
Next 
Set Re=nothing
If UploadFiles<>"" Then
UploadFiles=Right(UploadFiles,Len(UploadFiles)-1)
End If
ReplaceSaveRemoteFile=ConStr
End function
	
'过程名：SaveRemoteFile
'作 用：保存远程的文件到本地
'参 数：LocalFileName ------ 本地文件名
'参 数：RemoteFileUrl ------ 远程文件URL
'==================================================
Function SaveRemoteFile(LocalFileName,RemoteFileUrl)
On error resume next
SaveRemoteFile=True
  dim Ads,Retrieval,GetRemoteData
  Set Retrieval = Server.CreateObject("Microsoft.XMLHTTP")
  With Retrieval
    .Open "Get", RemoteFileUrl, False, "", ""
    .Send
If .Readystate<>4 then
SaveRemoteFile=False
Exit Function
End If
    GetRemoteData = .ResponseBody
  End With
  Set Retrieval = Nothing
  Set Ads = Server.CreateObject("Adodb.Stream")
  With Ads
    .Type = 1
    .Open
    .Write GetRemoteData
    .SaveToFile server.MapPath(LocalFileName),2
    .Cancel()
    .Close()
  End With
  Set Ads=nothing
end Function

'==================================================
'函数名：FpHtmlEnCode
'作 用：标题过滤
'参 数：fString ------字符串
'==================================================
Function FpHtmlEnCode(fString)
If IsNull(fString)=False or fString<>"" or fString<>"$False$" Then
fString=nohtml(fString)
fString=FilterJS(fString)
fString = Replace(fString, CHR(9), "")
fString = Replace(fString, CHR(34), "")
fString = Replace(fString, CHR(39), "")
fString = Replace(fString, CHR(13), "")
fString = Replace(fString, CHR(10), " ")
fString=Trim(fString)
fString=dvhtmlencode(fString)
FpHtmlEnCode=fString
Else
FpHtmlEnCode="$False$"
End If
End Function

'==================================================
'函数名：GetPaing
'作 用：获取分页
'==================================================
Function GetPaing(Byval ConStr,StartStr,OverStr,IncluL,IncluR)
If ConStr="$False$" or ConStr="" Or StartStr="" Or OverStr="" or IsNull(ConStr)=True or IsNull(StartStr)=True Or IsNull(OverStr)=True Then
GetPaing="$False$"
Exit Function
End If

Dim Start,Over,ConTemp,Erri
ConStr=LCase(ConStr)
StartStr=LCase(StartStr)
OverStr=LCase(OverStr)
Over=InstrB(1,ConStr,OverStr,vbBinaryCompare)
If Over<=0 Then
GetPaing="$False$"
Exit Function
Else
Over=Over+Lenb(OverStr)
End If

Start=Over-5
If Start<=0 Then
GetPaing="$False$"
Exit Function
End If

ConTemp=MidB(ConStr,Start,Over-Start)
Do While InstrB(1,ConTemp,StartStr,vbBinaryCompare)<=0
Erri=Erri+1
If Erri>50 then
GetPaing="$False$"
Exit Function
End If 
Start=Start-5
if Start<=0 then
GetPaing="$False$"
Exit Do
Exit Function
Else
ConTemp=MidB(ConStr,Start,Over-Start)
End If
Loop

Start=InstrB(1,ConTemp,StartStr,vbBinaryCompare)
If IncluL=False Then
Start=Start+LenB(StartStr)
End If
Over=InstrB(Start,ConTemp,OverStr,vbBinaryCompare)
If IncluR=True Then
Over=Over+LenB(OverStr)
End If
If Start>=Over then
GetPaing="$False$"
Exit Function
End If
GetPaing=MidB(ConTemp,Start,Over-Start)
GetPaing=Trim(GetPaing)
GetPaing=Replace(GetPaing," ","")
GetPaing=Replace(GetPaing,",","")
GetPaing=Replace(GetPaing,"'","")
GetPaing=Replace(GetPaing,"""","")
GetPaing=Replace(GetPaing,">","")
GetPaing=Replace(GetPaing,"<","")
End Function

'==================================================
'函数名：ScriptHtml
'作 用：过滤html标记
'参 数：ConStr ------ 要过滤的字符串
'==================================================
Function ScriptHtml(Byval ConStr,TagName,FType)
Dim Re
Set Re=new RegExp
Re.IgnoreCase =true
Re.Global=True
Select Case FType
Case 1
Re.Pattern="<" & TagName & "([^>])*>"
ConStr=Re.Replace(ConStr,"")
Case 2
Re.Pattern="<" & TagName & "([^>])*>.*?</" & TagName & "([^>])*>"
ConStr=Re.Replace(ConStr,"")
Case 3
Re.Pattern="<" & TagName & "([^>])*>"
ConStr=Re.Replace(ConStr,"")
Re.Pattern="</" & TagName & "([^>])*>"
ConStr=Re.Replace(ConStr,"")
End Select
ScriptHtml=ConStr
Set Re=Nothing
End Function

Function CheckDir(byval FolderPath)
  dim fso
  Set fso = Server.CreateObject("Scripting.FileSystemObject")
  If fso.FolderExists(Server.MapPath(folderpath)) then
  '存在
    CheckDir = True
  Else
  '不存在
    CheckDir = False
  End if
  Set fso = nothing
End Function
Function MakeNewsDir(byval foldername)
  dim fso
  Set fso = Server.CreateObject("Scripting.FileSystemObject")
fso.CreateFolder(Server.MapPath(foldername))
If fso.FolderExists(Server.MapPath(foldername)) Then
MakeNewsDir = True
Else
MakeNewsDir = False
End If
  Set fso = nothing
End Function

'**************************************************
'函数名：IsObjInstalled
'作 用：检查组件是否已经安装
'参 数：strClassString ----组件名
'返回值：True ----已经安装
' False ----没有安装
'**************************************************
Function IsObjInstalled(strClassString)
  On Error Resume Next
  IsObjInstalled = False
  Err = 0
  Dim xTestObj
  Set xTestObj = Server.CreateObject(strClassString)
  If 0 = Err Then IsObjInstalled = True
  Set xTestObj = Nothing
  Err = 0
End Function

'**************************************************
'过程名：WriteErrMsg
'作 用：显示错误提示信息
'参 数：无
'**************************************************
sub WriteErrMsg(ErrMsg)
  dim strErr
  strErr=strErr & "<html><head><title>错误信息</title><meta http-equiv='Content-Type' content='text/html; charset=gb2312'>" & vbcrlf
  strErr=strErr & "<link href='../admin/Admin_STYLE.CSS' rel='stylesheet' type='text/css'></head><body><br><br>" & vbcrlf
  strErr=strErr & "<table cellpadding=2 cellspacing=1 border=0 width=400 class='border' align=center>" & vbcrlf
  strErr=strErr & " <tr align='center' class='title'><td height='22'><strong>错误信息</strong></td></tr>" & vbcrlf
  strErr=strErr & " <tr class='tdbg'><td height='100' valign='top'><b>产生错误的可能原因：</b>" & ErrMsg &"</td></tr>" & vbcrlf
  strErr=strErr & " <tr align='center' class='tdbg'><td><a href='javascript:history.go(-1)'>&lt;&lt; 返回上一页</a></td></tr>" & vbcrlf
  strErr=strErr & "</table>" & vbcrlf
  strErr=strErr & "</body></html>" & vbcrlf
  response.write strErr
end sub

'**************************************************
'过程名：WriteSucced
'作 用：显示成功提示信息
'参 数：无
'**************************************************
sub WriteSucced(ErrMsg)
  dim strErr
  strErr=strErr & "<html><head><title>成功信息</title><meta http-equiv='Content-Type' content='text/html; charset=gb2312'>" & vbcrlf
  strErr=strErr & "<link href='../admin/Admin_STYLE.CSS' rel='stylesheet' type='text/css'></head><body><br><br>" & vbcrlf
  strErr=strErr & "<table cellpadding=2 cellspacing=1 border=0 width=400 class='border' align=center>" & vbcrlf
  strErr=strErr & " <tr align='center' class='title'><td height='22'><strong>恭喜你！</strong></td></tr>" & vbcrlf
  strErr=strErr & " <tr class='tdbg'><td height='100' valign='top' align='center'>" & ErrMsg &"</td></tr>" & vbcrlf
  'strErr=strErr & " <tr align='center' class='tdbg'><td><a href='javascript:history.go(-1)'>&lt;&lt; 返回上一页</a></td></tr>" & vbcrlf
  strErr=strErr & "</table>" & vbcrlf
  strErr=strErr & "</body></html>" & vbcrlf
  response.write strErr
end sub

'**************************************************
'函数名：ShowPage
'作 用：显示“上一页 下一页”等信息
'参 数：sFileName ----链接地址
' TotalNumber ----总数量
' MaxPerPage ----每页数量
' ShowTotal ----是否显示总数量
' ShowAllPages ---是否用下拉列表显示所有页面以供跳转。有某些页面不能使用，否则会出现JS错误。
' strUnit ----计数单位
'返回值：“上一页 下一页”等信息的HTML代码
'**************************************************
function ShowPage(sFileName,TotalNumber,MaxPerPage,ShowTotal,ShowAllPages,strUnit)
  dim TotalPage,strTemp,strUrl,i

  if TotalNumber=0 or MaxPerPage=0 or isNull(MaxPerPage) then
    ShowPage=""
    exit function
  end if
  if totalnumber mod maxperpage=0 then
  TotalPage= totalnumber \ maxperpage
  else
  TotalPage= totalnumber \ maxperpage+1
  end if
  if CurrentPage>TotalPage then CurrentPage=TotalPage
    
  strTemp= "<table align='center'><tr><td>"
  if ShowTotal=true then 
    strTemp=strTemp & "共 <b>" & totalnumber & "</b> " & strUnit & "&nbsp;&nbsp;"
  end if
  strUrl=JoinChar(sfilename)
  if CurrentPage<2 then
  strTemp=strTemp & "首页 上一页&nbsp;"
  else
  strTemp=strTemp & "<a href='" & strUrl & "page=1'>首页</a>&nbsp;"
  strTemp=strTemp & "<a href='" & strUrl & "page=" & (CurrentPage-1) & "'>上一页</a>&nbsp;"
  end if

  if CurrentPage>=TotalPage then
  strTemp=strTemp & "下一页 尾页"
  else
  strTemp=strTemp & "<a href='" & strUrl & "page=" & (CurrentPage+1) & "'>下一页</a>&nbsp;"
  strTemp=strTemp & "<a href='" & strUrl & "page=" & TotalPage & "'>尾页</a>"
  end if
  strTemp=strTemp & "&nbsp;页次：<strong><font color=red>" & CurrentPage & "</font>/" & TotalPage & "</strong>页 "
  strTemp=strTemp & "&nbsp;<b>" & maxperpage & "</b>" & strUnit & "/页"
  if ShowAllPages=True then
    strTemp=strTemp & "&nbsp;&nbsp;转到第<input type='text' name='page' size='3' maxlength='5' value='" & CurrentPage & "' onKeyPress=""if (event.keyCode==13) window.location='" & strUrl & "page=" & "'+this.value;""'>页"
  end if
  strTemp=strTemp & "</td></tr></table>"
  ShowPage=strTemp
end function

'**************************************************
'函数名：JoinChar
'作 用：向地址中加入 ? 或 &
'参 数：strUrl ----网址
'返回值：加了 ? 或 & 的网址
'**************************************************
function JoinChar(strUrl)
  if strUrl="" then
    JoinChar=""
    exit function
  end if
  if InStr(strUrl,"?")<len(strUrl) then 
    if InStr(strUrl,"?")>1 then
      if InStr(strUrl,"&")<len(strUrl) then 
        JoinChar=strUrl & "&"
      else
        JoinChar=strUrl
      end if
    else
      JoinChar=strUrl & "?"
    end if
  else
    JoinChar=strUrl
  end if
end function

'**************************************************
'函数名：CreateKeyWord
'作 用：由给定的字符串生成关键字
'参 数：Constr---要生成关键字的原字符串
'返回值：生成的关键字
'**************************************************
Function CreateKeyWord(byval Constr)
If Constr="" or IsNull(Constr)=True or Constr="$False$" Then
CreateKeyWord="$False$"
Exit Function
End If
Constr=Replace(Constr,CHR(32),"")
Constr=Replace(Constr,CHR(9),"")
Constr=Replace(Constr,"&nbsp;","")
Constr=Replace(Constr," ","")
Constr=Replace(Constr,"(","")
Constr=Replace(Constr,")","")
Constr=Replace(Constr,"<","")
Constr=Replace(Constr,">","")
Dim i,ConstrTemp
For i=1 To Len(Constr)
ConstrTemp=ConstrTemp & "|" & Mid(Constr,i,2)
Next
If Len(ConstrTemp)<254 Then
ConstrTemp=ConstrTemp & "|"
Else
ConstrTemp=Left(ConstrTemp,254) & "|"
End If
CreateKeyWord=ConstrTemp
End Function

Function CheckUrl(strUrl)
Dim Re
Set Re=new RegExp
Re.IgnoreCase =true
Re.Global=True
Re.Pattern="http://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?"
If Re.test(strUrl)=True Then
CheckUrl=strUrl
Else
CheckUrl="$False$"
End If
Set Rs=Nothing
End Function

%>