//js和jsx的交互接口
var cs = new CSInterface();
//创建按钮点击
document.getElementById("btnCut").addEventListener("click",function(){
    var action = document.getElementById("action").action.value;
    //alert(save_format);
    //alert("cutAndSave('"+action+"','0')");
    cs.evalScript("cutAndSave('"+action+"','0')");
	//alert(action);
})

document.getElementById("btnCut_logo").addEventListener("click",function(){
    var action = document.getElementById("action").action.value;
    //alert(save_format);
    //alert("cutAndSave('"+save_format+"','"+action+"')")
    cs.evalScript("cutAndSave('"+action+"','1')");
	//alert(action);"cutAndSave('"+action+"',
})
document.getElementById("btnCut_banquan").addEventListener("click",function(){
    var action = document.getElementById("action").action.value;
    //alert(save_format);
    //alert("cutAndSave('"+save_format+"','"+action+"')")
    cs.evalScript("cutAndSave('"+action+"','2')");
	//alert(action);
})
document.getElementById("btnCut_noNeed").addEventListener("click",function(){
    var action = document.getElementById("action").action.value;
    var info_flag = document.getElementById("action").info_alert.checked;
    //alert(save_format);
    //alert("SaveDirect('"+action+"','2'"+info_flag+")");
    cs.evalScript("SaveDirect('"+action+"','0',"+info_flag+")");
	//alert(action);
})

document.getElementById("btn_close").addEventListener("click",function(){
	var info_flag = document.getElementById("action").info_alert.checked;
	//alert(info_flag);
	cs.evalScript("closeDoc("+info_flag+")");
})


/* document.getElementById("btnResizeImage").addEventListener("click",function(){
    cs.evalScript("resizeImageSize()");
})

 */
