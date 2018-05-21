function SetData (elem) {
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
} 

/*if(radioArr.indexOf(elem.getAttribute('id')) == -1 ) radioArr.push(elem.getAttribute('id'));
	else radioArr.splice(radioArr.indexOf(elem.getAttribute('id')), 1);
	*/

function SetCheckBox (elem) {
	var chekboxArr = [];
	chekboxArr =   JSON.parse(localStorage.getItem("chekboxArr"));
	if(chekboxArr==null)	chekboxArr = [];
	if(elem.checked) {
		if(chekboxArr.indexOf(elem.getAttribute('id')) == -1) chekboxArr.push(elem.getAttribute('id'));	
	}	
	else {
		if(chekboxArr.indexOf(elem.getAttribute('id')) != -1) chekboxArr.splice(chekboxArr.indexOf(elem.getAttribute('id')), 1);
	}

	localStorage.setItem("chekboxArr", JSON.stringify(chekboxArr));
} 


function GetData (item) { 
    return localStorage.getItem(item); 
}


window.onload = function() {
	localStorage.setItem("foldersImgAmmount", JSON.stringify([10,8])); // только для теста массив папок с количеством изображений в них
	localStorage.setItem("imgammount", 18 ); // только для теста  сколько всего изображений

	var imgammount = localStorage.getItem("imgammount"); 
	var foldersImgAmmount =  JSON.parse(localStorage.getItem("foldersImgAmmount"));					  


	var radioArr = [];
	radioArr =  JSON.parse(localStorage.getItem("radioArr"));	
	if(radioArr!=null) 
		for (var i = 0 ; i < radioArr.length; i++ ) {
			 if(document.getElementById(radioArr[i])!=null)
			 document.getElementById(radioArr[i]).checked = true;
		}

	var chekboxArr = [];
	chekboxArr =  JSON.parse(localStorage.getItem("chekboxArr"));	
	if(chekboxArr!=null) {
		for (var i = 0 ; i < chekboxArr.length; i++ ) {
 			 
 			if(document.getElementById(chekboxArr[i])!=null && chekboxArr[i]!=null){
 				document.getElementById(chekboxArr[i]).checked = true;
 				console.log(document.getElementsByName(chekboxArr[i])[0]);

 				console.log(chekboxArr[i]);
 				document.getElementsByName(chekboxArr[i])[0].className+=" checking";
 			}
			
			 
		}
	}

}