function myFunction() {

  var rushSheetId = "1i7dqF4c-e_-WLIXoKiv_8a6zIl21KPx19IkSvoXRKPk"; // rush headshot sheet id
	var slideShowName = 'Bid Selection Slides';

  var rushProfValues = getRushProfileValues(rushSheetId);

  var pres = SlidesApp.create(slideShowName);
  var sheet = SpreadsheetApp.getActiveSheet();

  pres.appendSlide()
  .insertTextBox("AKPSI Bid Selection");

  var data = sheet.getDataRange().getValues();
  for (var i =1; i < data.length; i++) {
    var newRushSlide = pres.appendSlide();
    Logger.log('Line: ' + data[i]);
    var rushRow = data[i];

    var matchResult;
    var rushId = rushRow[1];

    matchResult = matchSignInToRushProfile(rushProfValues, rushId); 
    
    if(matchResult === "NO MATCH"){
	    Logger.log("No match found for " + rushRow);
      return;
	  } else {
      rushName = matchResult[0];
      prePhotoUrl = matchResult[2];

      // get the picture and add it
      var sharingImgId = parseIdFromGoogleLink(prePhotoUrl);
      var imgId = removeViewFromGoogleSharingLink(sharingImgId);

      // might need to use getFileByIdAndResourceKey()
      var imageFile = DriveApp.getFileById(imgId);
      var blob = imageFile.getBlob();
      
      newRushSlide.insertImage(blob, 5, 20, 250, 400);
	  }

    var position = {left: 260, top: 10}
    
    var rushNameBox = newRushSlide
    .insertTextBox(rushRow[0] + " (" + rushRow[10] + ") - " + rushRow[9], 5, 4, 750, 30);

    var rushNameTextRange = rushNameBox.getText();
    rushNameTextRange.getTextStyle()
    .setFontSize(26);
    
    // newRushSlide
    // .insertTextBox("PSU ID: " + rushRow[1], position.left, 40, 500, 30);

    var rushWSBlock = newRushSlide
    .insertTextBox("Rush Week Score: " + rushRow[8], position.left, 60, 500, 30);

    makeTextBig(rushWSBlock, 18);

    var rushInterviewBlock = newRushSlide
    .insertTextBox("Interview: " + rushRow[4] + " (" + rushRow[5] + ")", position.left, 100, 500, 30);

    makeTextBig(rushInterviewBlock, 18);

    var pmTextBlock = newRushSlide
    .insertTextBox("PM: " + rushRow[6], position.left, 130, 200, 30);

    makeTextBig(pmTextBlock, 18);

    var rushTextBlock = newRushSlide
    .insertTextBox("Rush: " + rushRow[7], position.left + 200, 130, 200, 30);

    makeTextBig(rushTextBlock, 18);

    // gpa
    var gpaTB = newRushSlide
    .insertTextBox("GPA: " + rushRow[13], position.left + 200, 160, 200, 30);

    makeTextBig(gpaTB, 18);

    //involvements
    var invTB = newRushSlide
    .insertTextBox("Involvements: " + rushRow[12], position.left, 210, 450, 50);

    makeTextBig(invTB, 18);

    // prev knowns
    var prevKnownTB = newRushSlide
    .insertTextBox("Previously Knowns: " + rushRow[11], position.left, 310, 450, 50);

    makeTextBig(prevKnownTB, 18);
  }

  Logger.log('Published URL: ' + pres.getUrl());
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

function makeTextBig(textBlock, textSize){
  var rushNameTextRange = textBlock.getText();
    rushNameTextRange.getTextStyle()
    .setFontSize(textSize);
}
      
function getRushProfileValues(rushProfSheetId){
	var rushProfSheet = SpreadsheetApp.openById(rushProfSheetId);
	var data = rushProfSheet.getDataRange().getValues();
	return data;
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
  // Logger.log("the index " + idEqualIndex + " will be used to get " + imgUrl);
  // Logger.log("parsed id is " + parsedId);
  return parsedId;
}
