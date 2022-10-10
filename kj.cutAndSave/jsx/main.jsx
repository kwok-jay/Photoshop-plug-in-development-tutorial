function saveDoc_psd(currentDoc,path) {
    saveFilePath = new File(path);
    psdSaveOptions = new PhotoshopSaveOptions();
    currentDoc.saveAs(saveFilePath,psdSaveOptions , true, Extension.LOWERCASE);
    alert(path+'.psd：保存完成！')
    
}

function saveDoc_png(currentDoc,path){
    var saveFilePath = new File(path);
    var options = PNGSaveOptions;
    var asCopy = true;
    var extensionType = Extension.LOWERCASE;
    currentDoc.saveAs(saveFilePath, options, asCopy, extensionType);
    alert(path+'：保存完成！')
}

function getNum(new_path,save_format){
	var temp_path = ''
    for(var i=1;i<=50;i++){
        temp_path = new_path + i.toString()+ save_format
        var temp_file1 = new File(temp_path)
		temp_path = new_path + i.toString()+ 'logo' +save_format
        var temp_file2 = new File(temp_path)
		temp_path = new_path + i.toString()+ '版权' +save_format
        var temp_file3 = new File(temp_path)
		if ((temp_file1.exists)|(temp_file2.exists)|(temp_file3.exists)) {
			// alert(temp_path);
			continue;}
		else {
			//alert(i)
			return i.toString()
		}
	}
}

var cutAndSave = function (action,type) {
    //alert(type)
    //alert(action)
	var save_format='.psd'
    //裁剪
    var document = app.activeDocument;
    var bounds = app.activeDocument.selection.bounds;
    var angle = 0;
    document.crop(bounds, angle);

    //保存路径
    var currentFilename = (document.name).toString() //登录武林 01-.png
	//alert(currentFilename)
    var new_name_pre = currentFilename.slice(0,currentFilename.lastIndexOf('.'))
    // alert(new_name_pre+' new_name_pre')
    
    if (action=='1'){
        var save_dir_name = currentFilename.slice(0,currentFilename.indexOf('-'))
        var new_path = document.path+'/' + save_dir_name + '/' + new_name_pre
		//alert('a=1')
    }
    if (action=='2'){
        var save_dir_name = '《'+currentFilename.slice(0,currentFilename.indexOf(' '))+'》已裁剪'
        var new_path = document.path+'/' + save_dir_name + '/' + currentFilename.slice(0,currentFilename.indexOf('-')) + '/'+ new_name_pre
    }
    // alert(new_path+' new_path')

    new_path = new_path + getNum(new_path,save_format)
	//alert(new_path)
	if (type=='1'){new_path = new_path + 'logo'}
	if (type=='2'){new_path = new_path + '版权'}
	
    //if (save_format=='.png'){saveDoc_png(document,new_path)}
    saveDoc_psd(document,new_path)

    //回退
    var lastHistoryNum = document.historyStates.length - 2;
    document.activeHistoryState = document.historyStates[lastHistoryNum];
}

var closeDoc = function (info_flag) {

    var document = app.activeDocument;
	var file_name = (document.name).toString();
	document.close(SaveOptions.DONOTSAVECHANGES);
	if(info_flag){alert('文件已关闭：'+file_name);}
	
}

var SaveDirect = function (action,type,info_flag) {
    //alert(type)
    //alert(action)
    var save_format='.psd'
    //裁剪
    var document = app.activeDocument;

    //保存路径
    var currentFilename = (document.name).toString() //登录武林 01-.png
    //alert(currentFilename)
    var new_name_pre = currentFilename.slice(0,currentFilename.lastIndexOf('.'))
    // alert(new_name_pre+' new_name_pre')

    if (action=='1'){
        var save_dir_name = currentFilename.slice(0,currentFilename.indexOf('-'))
        var new_path = document.path+'/' + save_dir_name + '/' + new_name_pre
        //alert('a=1')
    }
    if (action=='2'){
        var save_dir_name = '《'+currentFilename.slice(0,currentFilename.indexOf(' '))+'》已裁剪'
        var new_path = document.path+'/' + save_dir_name + '/' + currentFilename.slice(0,currentFilename.indexOf('-')) + '/'+ new_name_pre
    }
    // alert(new_path+' new_path')

    new_path = new_path + getNum(new_path,save_format)
    //alert(new_path)
    if (type=='1'){new_path = new_path + 'logo'}
    if (type=='2'){new_path = new_path + '版权'}

    //if (save_format=='.png'){saveDoc_png(document,new_path)}
    saveDoc_psd(document,new_path)
    //关闭文件
    var file_name = (document.name).toString();
    document.close(SaveOptions.DONOTSAVECHANGES);
    if(info_flag){alert('文件已关闭：'+file_name);}

}

/* var resizeImageSize = function () {
	var document = app.activeDocument;
	document.resizeImage((UnitValue 1280 px),,300,ResampleMethod.AUTOMATIC)
} */