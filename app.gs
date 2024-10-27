function doGet(e) {

	var params = e.parameter;

	var SpreadSheet = SpreadsheetApp.openById("1i539gvSky_jC0sA0x2e6jZLpvnDtDpd_yP9H04mRhLQ");
	var Sheet = SpreadSheet.getSheetByName(params.mode);
	var LastRow = Sheet.getLastRow();

	Sheet.getRange(LastRow+1, 1).setValue(params.name);
	Sheet.getRange(LastRow+1, 2).setValue(params.mail);
	Sheet.getRange(LastRow+1, 3).setValue(params.version);
	Sheet.getRange(LastRow+1, 4).setValue(params.formid);
	Sheet.getRange(LastRow+1, 5).setValue(params.timestamp);

  // Questions, sub-questions, and comments
  var currentColumn = 6; // Starting column for question data

	for (var i = 1; i <= 20; i++) {
    // Main question response
    if (params.hasOwnProperty("q" + i)) {
      Sheet.getRange(LastRow+1, currentColumn).setValue(params["q" + i]);
      currentColumn++;
    }

    // Sub-questions and comments
    for (var j = 1; j <= 2; j++) {
      var subQuestionKey = "q" + i + "_" + j;
      var commentKey = subQuestionKey + "_comment";

      // Sub-question
      if (params.hasOwnProperty(subQuestionKey)) {
        Sheet.getRange(LastRow+1, currentColumn).setValue(params[subQuestionKey]);
        currentColumn++;
      }

      // Comment
      if (params.hasOwnProperty(commentKey)) {
        Sheet.getRange(LastRow+1, currentColumn).setValue(params[commentKey]);
        currentColumn++;
      }
    }
  }

	return ContentService.createTextOutput(params.thank);
}
