var foldersImgAmmount = 20 ; // folders ammount * 2

function loginBut()
{
	localStorage.removeItem("chekboxArr");
	localStorage.removeItem("radioArr");
	localStorage.removeItem("checkBoxDisabledArr");
     window.location = "main.html"
}

function SetData (elem) {
	var folderId = elem.getAttribute('radioGroupId');
	var radioArr = [];
	radioArr =  JSON.parse(localStorage.getItem("radioArr"));
	if(radioArr==null)	radioArr = [];

/*	radioArr[elem.getAttribute('radioGroupId')] = elem.getAttribute('id');*/

	if(radioArr.indexOf(elem.getAttribute('radioGroupId')) == -1 ){
		radioArr.push(elem.getAttribute('radioGroupId'));
		radioArr.push(elem.getAttribute('id'));
	}
	else{
		radioArr[radioArr.indexOf(elem.getAttribute('radioGroupId'))+1] = elem.getAttribute('id');
	}
	localStorage.setItem("radioArr", JSON.stringify(radioArr));

	if(radioArr.length==foldersImgAmmount) {
		document.getElementById("btnNext").disabled = false;
		if(document.getElementById("btnNext").classList.contains('btn-secondary')){
			document.getElementById("btnNext").classList.remove('btn-secondary');
			document.getElementById("btnNext").classList.add('btn-primary');
		}
	}
	// if radiobtn 2 or 3 we should disable all checkboxes in this folder
	var x = document.getElementsByName("checkbox"); // maybe updated

	if(elem.getAttribute('btnType')>0 && elem.getAttribute('btnType')<=3){
		for (var i = 0; i < x.length; i++) {
			if(x[i].getAttribute('filePathId')==folderId){
				x[i].checked = false;
				x[i].disabled = true;
				if (document.getElementsByName(x[i].getAttribute('id'))[0].classList.contains('checking')) {
 						document.getElementsByName(x[i].getAttribute('id'))[0].classList.remove('checking');
				}
			}

		}
		/// disable all cheboxes in local memory of browser
	}
	else{
		// load all from local data of browser
		var chekboxArr = [];
		chekboxArr =  JSON.parse(localStorage.getItem("chekboxArr"));
		if(chekboxArr!=null) {
			for (var i = 0 ; i < chekboxArr.length; i++ ) {
	 			if(document.getElementById(chekboxArr[i])!=null && chekboxArr[i]!=null && document.getElementById(chekboxArr[i]).getAttribute('filePathId')==folderId ){
	 				document.getElementById(chekboxArr[i]).checked = true;
	 			}
			}
		}

		for (var i = 0; i < x.length; i++) {
			if(x[i].getAttribute('filePathId')==folderId){
				x[i].disabled = false;
				if(x[i].checked==true){
					if (document.getElementsByName(x[i].getAttribute('id'))[0].classList.contains('checking')==false) {
 						document.getElementsByName(x[i].getAttribute('id'))[0].classList.add('checking');
					}
				}
			}
		}
	}
	updateCheckBoxDisabled(x);

}

function updateCheckBoxDisabled(elem){

	var checkBoxDisabledArr = [];
	checkBoxDisabledArr =   JSON.parse(localStorage.getItem("checkBoxDisabledArr"));
	if(checkBoxDisabledArr==null)	checkBoxDisabledArr = [];
	for (var i = 0; i < elem.length; i++) {
		if(elem[i].disabled) {
			if(checkBoxDisabledArr.indexOf(elem[i].getAttribute('id')) == -1) checkBoxDisabledArr.push(elem[i].getAttribute('id'));
		}
		else {
			if(checkBoxDisabledArr.indexOf(elem[i].getAttribute('id')) != -1) checkBoxDisabledArr.splice(checkBoxDisabledArr.indexOf(elem[i].getAttribute('id')), 1);
		}
	}


	localStorage.setItem("checkBoxDisabledArr", JSON.stringify(checkBoxDisabledArr));
}

function SetCheckBox (elem) {
	var chekboxArr = [];
	chekboxArr =   JSON.parse(localStorage.getItem("chekboxArr"));
	if(chekboxArr==null)	chekboxArr = [];
	if(elem.checked) {
		if(chekboxArr.indexOf(elem.getAttribute('id')) == -1) chekboxArr.push(elem.getAttribute('id'));
	}
	else {
		if(chekboxArr.indexOf(elem.getAttribute('id')) != -1) {
			chekboxArr.splice(chekboxArr.indexOf(elem.getAttribute('id')), 1);
		}
	}

	localStorage.setItem("chekboxArr", JSON.stringify(chekboxArr));
}


function GetData (item) {
    return localStorage.getItem(item);
}

function clickToImage(elem){

	var checkBoxElem = document.getElementById(elem.getAttribute("name")); // checkbox
	if(checkBoxElem.disabled == true ){
		
		var filepathIdFolder = checkBoxElem.getAttribute("filePathId"); // folder id 

		var inputs = document.getElementsByTagName('input'); // all inputs
		var radioArr = [];
		radioArr =  JSON.parse(localStorage.getItem("radioArr"));	// radiobuttons arr
		if(radioArr==null)	radioArr = [];

		var checkBoxDisabledArr = [];
		checkBoxDisabledArr =   JSON.parse(localStorage.getItem("checkBoxDisabledArr"));
		if(checkBoxDisabledArr==null)	checkBoxDisabledArr = [];

		var chekboxArr = [];
		chekboxArr =  JSON.parse(localStorage.getItem("chekboxArr"));	
		if(chekboxArr==null) chekboxArr = [];

		// deleting radio buttn check
		for(var i = 0; i < inputs.length; i++) {
		    if(inputs[i].type.toLowerCase() == 'radio') {

		        if(inputs[i].getAttribute("radioGroupId")==filepathIdFolder && inputs[i].checked==true){
		        	inputs[i].checked = false;
		        	if(radioArr!=null && radioArr.indexOf(filepathIdFolder)!=-1 ) radioArr.splice(radioArr.indexOf(filepathIdFolder),2);
		        }
		    }
		    else if(inputs[i].type.toLowerCase() == 'checkbox') {
		    	if(inputs[i].getAttribute("filePathId")==filepathIdFolder && checkBoxDisabledArr.indexOf(inputs[i].getAttribute("id"))!=-1){
		    		checkBoxDisabledArr.splice(checkBoxDisabledArr.indexOf(inputs[i].getAttribute("id")),1);
		    		inputs[i].disabled = false;	  
		    		if(chekboxArr.indexOf(inputs[i].getAttribute("id"))!=-1){
 						document.getElementsByName(inputs[i].getAttribute("id"))[0].classList.add('checking');
 						inputs[i].checked= true;
		    		}  				    		
		    	}
		    	
		    }
		}
		document.getElementById(elem.getAttribute("name")).checked = false;
		if(elem.classList.contains('checking')==true) elem.classList.remove('checking'); // для обработчика нажатия на это изображения нужно удалить.
		localStorage.setItem("radioArr", JSON.stringify(radioArr));
		localStorage.setItem("checkBoxDisabledArr", JSON.stringify(radioArr));
		localStorage.setItem("chekboxArr", JSON.stringify(chekboxArr));

		document.getElementById("btnNext").disabled = true;
			if(document.getElementById("btnNext").classList.contains('btn-primary')){
				document.getElementById("btnNext").classList.remove('btn-primary');	
				document.getElementById("btnNext").classList.add('btn-secondary');
		}

	}

	if(document.getElementById(elem.getAttribute("name"))!=null && document.getElementById(elem.getAttribute("name")).disabled==false){
		if(elem.classList.contains('checking')==false)
				elem.classList.add('checking');
		else 	elem.classList.remove('checking');
	}

}


window.onload = function() {
/*	localStorage.setItem("foldersImgAmmount", JSON.stringify([10,8])); // только для теста массив папок с количеством изображений в них
	localStorage.setItem("imgammount", 18 ); // только для теста  сколько всего изображений

	var imgammount = localStorage.getItem("imgammount");
	var foldersImgAmmount =  JSON.parse(localStorage.getItem("foldersImgAmmount"));*/
	foldersImgAmmount = (document.getElementsByClassName("funkyradio").length) * 2;
	var radioArr = [];
	radioArr =  JSON.parse(localStorage.getItem("radioArr"));
	if(radioArr!=null)
		for (var i = 0 ; i < radioArr.length; i++ ) {
			 if(document.getElementById(radioArr[i])!=null)
			 document.getElementById(radioArr[i]).checked = true;
		}
	if(radioArr!=null) {
		if(radioArr.length==foldersImgAmmount){
			document.getElementById("btnNext").disabled = false;
			if(document.getElementById("btnNext").classList.contains('btn-secondary')){
				document.getElementById("btnNext").classList.remove('btn-secondary');
				document.getElementById("btnNext").classList.add('btn-primary');
			}
		}

	}

	var chekboxArr = [];
	chekboxArr =  JSON.parse(localStorage.getItem("chekboxArr"));	
	if(chekboxArr!=null) {
		for (var i = 0 ; i < chekboxArr.length; i++ ) {
 			 
 			if(document.getElementById(chekboxArr[i])!=null && chekboxArr[i]!=null){
 				document.getElementById(chekboxArr[i]).checked = true;
 				document.getElementsByName(chekboxArr[i])[0].className+=" checking";
 			}
			
			 
		}
	}

	/// disable all find locked checkboxes
	var checkBoxDisabledArr = [];
	checkBoxDisabledArr =  JSON.parse(localStorage.getItem("checkBoxDisabledArr"));	
	if(checkBoxDisabledArr!=null) {
		for (var i = 0 ; i < checkBoxDisabledArr.length; i++ ) {
 			 
 			if(document.getElementById(checkBoxDisabledArr[i])!=null && checkBoxDisabledArr[i]!=null){
 				document.getElementById(checkBoxDisabledArr[i]).disabled = true;
 				document.getElementById(checkBoxDisabledArr[i]).checked = false;
 				if(document.getElementsByName(checkBoxDisabledArr[i])[0].classList.contains('checking')){
 					document.getElementsByName(checkBoxDisabledArr[i])[0].classList.remove('checking');		
 				}	
 			}
			
			 
		}
	}

}