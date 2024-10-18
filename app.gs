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

	for (var i = 1; i <= 20; i++) {
		Sheet.getRange(LastRow+1, 5+i).setValue(params["q" + i.toString()]);
	}

	return ContentService.createTextOutput(params.thank);
}
