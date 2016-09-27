function getCookie(c_name)
{
	if (document.cookie.length>0){
		c_start=document.cookie.indexOf(c_name + "=")
		if (c_start!=-1){
			c_start=c_start + c_name.length+1 
			c_end=document.cookie.indexOf(";",c_start)
			if (c_end==-1)
				c_end=document.cookie.length
	    	return unescape(document.cookie.substring(c_start,c_end))
	    } 
	  }
	return ""
}


function swfUploadLoaded() {
	var btn_submit = document.getElementById("btn_submit");
	//get cookie
	var sessionid = getCookie("sessionid");
	swfu.upload_url += "?sessionid=" + sessionid;
	btn_submit.onclick = doSubmit;
	btn_submit.disabled = false;
}

function clearTips(){
    var ids = new Array("title_tips","tags_tips","channel_tips","descripiton_tips");
    for (var i = 0; i < ids.length; i++) {
      document.getElementById(ids[i]).innerText = "";
    };
}

function check_form(){
    clearTips();
    form_item = document.getElementById("upload_form");
    filetxt = document.getElementById("txtFileName");
    var value_array = new Array(form_item.title.value,form_item.tags.value,
                  form_item.channel.value,form_item.describe.value,filetxt.value);
    var id_array = new Array("title_tips","tags_tips","channel_tips","descripiton_tips","filename_tips");
    for(var index=0;index<value_array.length;index++){
      if(value_array[index] == ""){
        document.getElementById(id_array[index]).innerText = "不能为空";
        return false;
      }
    }
    return true;
  }

// Called by the submit button to start the upload
function doSubmit(e) {
	if(!check_form()){
		return false;
	}
	
	try {
		swfu.startUpload();
	} catch (ex) {

	}
	var btn_submit = document.getElementById("btn_submit");
	btn_submit.disabled = "disabled";
	var btn_cancel = document.getElementById("btn_cancel");
	btn_cancel.disabled = "";
	return false;
}

function fileDialogStart() {
	var txtFileName = document.getElementById("txtFileName");
	txtFileName.value = "";

	this.cancelUpload();
}

function fileQueueError(file, errorCode, message)  {
	try {
		// Handle this error separately because we don't want to create a FileProgress element for it.
		switch (errorCode) {
		case SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED:
			alert("You have attempted to queue too many files.\n" + (message === 0 ? "You have reached the upload limit." : "You may select " + (message > 1 ? "up to " + message + " files." : "one file.")));
			return;
		case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
			alert("The file you selected is too big.");
			this.debug("Error Code: File too big, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
			alert("The file you selected is empty.  Please select another file.");
			this.debug("Error Code: Zero byte file, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		case SWFUpload.QUEUE_ERROR.INVALID_FILETYPE:
			alert("The file you choose is not an allowed file type.");
			this.debug("Error Code: Invalid File Type, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		default:
			alert("An error occurred in the upload. Try again later.");
			this.debug("Error Code: " + errorCode + ", File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			return;
		}
	} catch (e) {
	}
}

function fileQueued(file) {
	try {
		var txtFileName = document.getElementById("txtFileName");
		txtFileName.value = file.name;
	} catch (e) {
	}

}
function fileDialogComplete(numFilesSelected, numFilesQueued) {
	
}

function uploadProgress(file, bytesLoaded, bytesTotal) {
	try {
		var percent = "" + Math.ceil(bytesLoaded * 100 / bytesTotal ) + "%";
		updateProgress(percent);
	} catch (e) {
	}
}

function uploadSuccess(file, serverData) {
	try {
		var btn_cancel = document.getElementById("btn_cancel");
		btn_cancel.disabled = "disabled";
		var result = eval('('+serverData+')');
        if(result.result == "ok"){
          	document.getElementById("hidFileID").value = result.fileid;
          	document.getElementById("upload_form").submit();
        }else{
        	alert(result.err);
        	reset();
        }
	} catch (e) {
	}
}

function uploadError(file, errorCode, message) {
	try {
		if (errorCode === SWFUpload.UPLOAD_ERROR.FILE_CANCELLED) {
			reset();
		}
		
		var txtFileName = document.getElementById("txtFileName");
		txtFileName.value = "";
		
		// Handle this error separately because we don't want to create a FileProgress element for it.
		switch (errorCode) {
		case SWFUpload.UPLOAD_ERROR.MISSING_UPLOAD_URL:
		//	alert("There was a configuration error.  You will not be able to upload a resume at this time.");
			alert("上传控件配置错误");
			this.debug("Error Code: No backend file, File name: " + file.name + ", Message: " + message);
			break;
		case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
			alert("你只能上传一个文件");
			this.debug("Error Code: Upload Limit Exceeded, File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			break;
		case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
		case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
			break;
		default:
			alert("有错误发生，请稍后重试");
			this.debug("Error Code: " + errorCode + ", File name: " + file.name + ", File size: " + file.size + ", Message: " + message);
			break;
		}
		reset();
	}catch(e){

	}
}

function uploadComplete(file) {
	try {

	} catch (e) {
	}
}

function reset(){
    updateProgress("0%");
    var btn_submit = document.getElementById("btn_submit");
    btn_submit.disabled = "";
    var btn_cancel = document.getElementById("btn_cancel");
    btn_cancel.disabled = "disabled";
    swfu.cancelUpload();
    document.getElementById("txtFileName").value = "";
}

function updateProgress(progress){
	var progressbar = document.getElementById("progressbar");
    progressbar.style.width = progress;
    var label = document.getElementById("progress_label");
    label.innerText = progress;
    return ;
}

function cancel_submit(){
	swfu.cancelUpload();
}