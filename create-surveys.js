function myFunction() {
	/*
	  change these values when we run it
	*/
      
	var rushSheetId = "1erMvJNC12UrzN_sJBHV8fpALMF72qmOKP9r6ZOY7o_M";
	var eventFormName = "Mock Random Ass Test Form";
      
	// Don't change anything below
	var sheet = SpreadsheetApp.getActiveSpreadsheet();
	var formRushCount = 0;
	var formCount = 0;
	var forms = [];
      
      
	var form = createNewBroRespForm(eventFormName, formCount);
	forms.push(form);
      
	var signInData = sheet.getDataRange().getValues();
	var rushProfValues = getRushProfileValues(rushSheetId);
	var activeForm;
      
	// iterate thru and match the mock rush responses sheet
	// make blocks of 40 rushes per form
	for (var i = 1; i < signInData.length; i++) {
	  if(formRushCount === 40){
	    formCount = formCount + 1;
	    form = createNewBroRespForm(eventFormName, formCount);
	    
	    forms.push(form);
	    formRushCount = 0;
	  }
	  activeForm = forms[formCount];
	  
	  signInRow = signInData[i];
	  signInId = signInRow[1];
      
	  matchResult = matchSignInToRushProfile(rushProfValues, signInId);
      
	  if(matchResult === "NO MATCH"){
	    Logger.log("No match found for " + signInRow);
	  } else {
      rushName = matchResult[0];
      prePhotoUrl = matchResult[2];

	    // create the signin form
	    activeForm.addPageBreakItem()
	    .setTitle("New Rush");
      
	    activeForm.addSectionHeaderItem()
	    .setTitle(rushName);
      
	    activeForm.addTextItem()
	    .setTitle(rushName + "/" +rushId);

      // get the picture and add it
      var sharingImgId = parseIdFromGoogleLink(prePhotoUrl);
      var imgId = removeViewFromGoogleSharingLink(sharingImgId);

      // might need to use getFileByIdAndResourceKey()
      var imageFile = DriveApp.getFileById(imgId);
      var blob = imageFile.getBlob();

      activeForm.addImageItem()
      .setTitle("Rush Photo")
      .setHelpText("this is a photo of a rush")
      .setImage(blob);
      
	    addSurveyQuestionsForRush(activeForm, rushName);
	    formRushCount = formRushCount + 1;
	  }
	}
      
      
	logAllFormUrls(forms);
}
      
function logAllFormUrls(forms){
	Logger.log("Logging all form urls")
	for (var i = 0; i < forms.length; i++){
		Logger.log("Form " + i + ": " + forms[i].getEditUrl());
	}
}

function createNewBroRespForm(formName, formCount){
	var form = FormApp.create(formName + "-" + formCount);
	form.addTextItem()
		.setTitle("Brother PSU ID");

	return form;
}
      
function matchSignInToRushProfile(rushProfileData, signInId){
	//Logger.log("matching id: " + signInId);
	for (var i = 1; i < rushProfileData.length; i++) {
		rushRow = rushProfileData[i];
		rushId = rushRow[1];

		if(rushId === signInId) {
		Logger.log("found a match " + rushRow)
		return rushRow;
		}
	}

	return "NO MATCH";
}
      
function getRushProfileValues(rushProfSheetId){
	var rushProfSheet = SpreadsheetApp.openById(rushProfSheetId);
	var data = rushProfSheet.getDataRange().getValues();
	return data;
}
      
function addSurveyQuestionsForRush(form, rushName) {
	form.addMultipleChoiceItem()
		.setTitle('Did you meet this rush?')
		.setChoiceValues(['Yes','No']);

	form.addMultipleChoiceItem()
		.setTitle('Did ' + rushName + ' act appropriately in the given environment?')
		.setChoiceValues(['Strongly Agree','Agree', "Neutral", 'Disagree', 'Strongly Disagree']);

	form.addMultipleChoiceItem()
		.setTitle('Did ' + rushName + ' have goals and aspirations? (did they seem motivated or passionate talking about an experience/anything)')
		.setChoiceValues(['Strongly Agree','Agree', "Neutral", 'Disagree', 'Strongly Disagree']);

	form.addMultipleChoiceItem()
		.setTitle('Did you enjoy talking to ' + rushName + '? (would you have continued the conversation if time didn’t go up/was the rush dry)')
		.setChoiceValues(['Strongly Agree','Agree', "Neutral", 'Disagree', 'Strongly Disagree']);

	form.addMultipleChoiceItem()
		.setTitle('Would ' + rushName + ' be a good addition to the network of akpsi? (will they help with future pledge classes, will they be involved)?')
		.setChoiceValues(['Strongly Agree','Agree', "Neutral", 'Disagree', 'Strongly Disagree']);

	form.addParagraphTextItem()
		.setTitle('Add any additional comments you may have on ' + rushName);
}

function parseIdFromGoogleLink(imgUrl){
  var idEqualIndex = -1;

  var parsedId = "";

  for (var char = 0; char < imgUrl.length; char++){
    var cur = imgUrl[char];
    if(idEqualIndex != -1) {
      parsedId += imgUrl[char];
    }

    if (char - 2 > 0) {
      if(cur == "/" && imgUrl[char - 1] == "d"){
        if (imgUrl[char - 2] == "/") {
          idEqualIndex = char;
        }
      }
    }
  }
  // Logger.log("the index " + idEqualIndex + " will be used to get " + imgUrl);
  // Logger.log("parsed id is " + parsedId);
  return parsedId;
}

function removeViewFromGoogleSharingLink(imgUrl) {
  var idEqualIndex = -1;

  var parsedId = "";
  // Logger.log("here is the second url " + imgUrl);

  for (var char = 0; char < imgUrl.length; char++){
    var cur = imgUrl[char];
    if(idEqualIndex == -1) {
      parsedId += imgUrl[char];
    }

    if (char + 4 < imgUrl.length) {
      if(imgUrl[char + 1] == "/" && imgUrl[char + 2] == "v"){
        if (imgUrl[char + 3] == "i" && imgUrl[char + 4] == "e") {
          idEqualIndex = char;
        }
      }
    }
  }
  Logger.log("the index " + idEqualIndex + " will be used to get " + imgUrl);
  Logger.log("parsed id is " + parsedId);
  return parsedId;
}
