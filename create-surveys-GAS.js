function myFunction() {
	/*
	  Change these values when we run it
	*/
      
	var rushSheetId = "1i7dqF4c-e_-WLIXoKiv_8a6zIl21KPx19IkSvoXRKPk";
	var eventFormName = "SD FA25 Scoring Form";
      
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
  // 0 - 30 | 30 - 60 | 60 - 90 | 90 - 120 | 117 - 146 | 146 - 175 | 175 - 197
  // for (var i = 0; i < 39; i++) {
  // for (var i = 55; i < signInData.length; i++) {
	for (var i = 180; i < 210; i++) {
	  if(formRushCount === 30){
	    formCount = formCount + 1;
	    form = createNewBroRespForm(eventFormName, formCount);
	    
	    forms.push(form);
	    formRushCount = 0;
	  }
	  activeForm = forms[formCount];
	  
	  signInRow = signInData[i];
	  signInId = signInRow[2];
      
	  matchResult = matchSignInToRushProfile(rushProfValues, signInId);
      
	  if(matchResult === "NO MATCH"){
	    Logger.log("No match found for " + signInRow);
      return;
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
	for (var i = 1; i < forms.length; i++){
		Logger.log("Form " + i + ": " + forms[i].getEditUrl());
	}
}

function createNewBroRespForm(formName, formCount){
	var form = FormApp.create(formName + "-" + formCount);
	form.addTextItem()
		.setTitle("Brother PSU ID (abc1234)")
    .setRequired(true);

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
		.setChoiceValues(['Yes','No'])
    .setRequired(true);

	form.addMultipleChoiceItem()
		.setTitle('Did ' + rushName + ' have goals and aspirations? (did they seem motivated or passionate talking about an experience/anything)')
		.setChoiceValues(['Strongly Agree','Agree', "Neutral", 'Disagree', 'Strongly Disagree']);

	form.addMultipleChoiceItem()
		.setTitle('Did you enjoy talking to ' + rushName + '? (would you have continued the conversation if time didn’t go up/was the rush not dry)')
		.setChoiceValues(['Strongly Agree','Agree', "Neutral", 'Disagree', 'Strongly Disagree']);

	form.addMultipleChoiceItem()
		.setTitle(rushName + ' would be a strong fit for the pledge class/fraternity')
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

    if (char - 2 > 0) {
      if(cur == "=" && imgUrl[char - 1] == "d"){
        if (imgUrl[char - 2] == "i") {
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