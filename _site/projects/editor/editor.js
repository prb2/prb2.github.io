var title;
var subtitle;
var filename;
var defaultText = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce accumsan nulla quam, vitae mollis massa lobortis eget. Donec quis accumsan quam, et auctor dui. Cras ultrices velit et mauris lobortis, et lobortis sapien commodo. Quisque lacinia rutrum dui nec interdum. Nulla lacinia nisi congue dapibus elementum. Mauris id dictum orci. Proin tincidunt massa ac lacinia consectetur. Quisque vitae nunc lobortis, malesuada augue at, auctor enim. Fusce vitae consectetur lectus. Curabitur tortor tortor, dictum placerat aliquet blandit, molestie in orci.\n \n Fusce sapien augue, vulputate vitae mauris lacinia, elementum efficitur nulla. Sed tristique vehicula consequat. Suspendisse condimentum ut lorem vitae suscipit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus efficitur erat et purus varius, ac aliquet urna consectetur. Aliquam erat volutpat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Pellentesque elementum tellus justo, eget ultrices libero porta et. Nam ornare pharetra velit sit amet faucibus. Quisque ut feugiat odio. Nam risus ipsum, porta in est ac, malesuada faucibus ante. Nunc iaculis scelerisque rutrum.';			


function setOptions(){
	title = document.getElementById("title").value;
	subtitle = document.getElementById("subtitle").value;
	if(title == ""){
		filename = "NewEdit.txt";
	} else {
		filename = title + ".txt";
	}
	
	document.getElementById("main").innerHTML = createEditorHTML(title, subtitle);
}


function newEditor(){
	window.location.reload();
}

function save(){
	console.log(filename);
	
	var textToSave = title + "\n" + subtitle + "\n\n" + document.getElementById("inputText").value;
	console.log(textToSave.value);
	
	var textBlob = new Blob([textToSave], {type:'text/plain'});
	console.log(textBlob);
	
	var link = document.createElement("a");
	link.download = filename;
	link.innerHTML = "Save edited text";
	
	window.URL = window.URL || window.webkitURL;
	link.href = window.URL.createObjectURL(textBlob);
	link.onclick = destroyClickedElement;
	link.style.display = "none";
	link.target = "_blank";
	link.name = "test";
	document.body.appendChild(link);
	link.click();
}

function destroyClickedElement(event)
{
    document.body.removeChild(event.target);
}

function createEditorHTML(){
	return '<center>\n'
	+ '<div class="title" id="inputTitle">\n'
	+ title + '\n'
	+'</div>\n' 
	+ '<div class="subtitle" id="inputSubtitle">\n'
	+ subtitle + '\n'
	+'</div>\n' 
	+ '<hr NOSHADE>'
	+'<textarea id="inputText" spellcheck="true" placeholder="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce accumsan nulla quam, vitae mollis massa lobortis eget. Donec quis accumsan quam, et auctor dui. Cras ultrices velit et mauris lobortis, et lobortis sapien commodo. Quisque lacinia rutrum dui nec interdum. Nulla lacinia nisi congue dapibus elementum. Mauris id dictum orci. Proin tincidunt massa ac lacinia consectetur. Quisque vitae nunc lobortis, malesuada augue at, auctor enim. Fusce vitae consectetur lectus. Curabitur tortor tortor, dictum placerat aliquet blandit, molestie in orci."></textarea>\n'
	+'</center>\n'
	+ '<div class="options">\n'
	+ '<button class="button" onclick="newEditor()">New</button>'
	+ '<button class="button" onclick="save()">Save</button>'
	+ '</div>\n'
}