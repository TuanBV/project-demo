import { cloneDeep } from 'lodash';
import dayjs from 'dayjs';
import { COLUMN_SEARCH, EVALUATE } from './const.js';

/**
 * Handle normalize and to lowser case character
 *
 * @param string|null character
 * @example normalizeCharacter('Nguyễn Văn A') -> nguyen van a
 * @returns string Normalized characters
 */
const normalizeCharacter = (character) => {
  const str = character === null ? '' : String(character);
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
};

// Filter interview date from
// Params:
//   @dataSearch: Data search
//   @element: Key name
//   @item: Data of candidate
//   @flagValid: Flag item valid with filter
// Output:
//   return: Flag of item
const filterInterviewDateFrom = (dataSearch, element, item, flagValid) => {
  const timeData = item.date !== null && item.date !== '' ? dayjs(item.date).toDate() : null;
  const timeSearch = dayjs(dataSearch.advance[element]).toDate();
  if (dataSearch.advance[element] !== null && timeData < timeSearch) {
    flagValid = false;
  }

  return flagValid;
};

// Filter interview date from
// Params:
//   @dataSearch: Data search
//   @element: Key name
//   @item: Data of candidate
//   @flagValid: Flag item valid with filter
// Output:
//   return: Flag of item
const filterInterviewDateTo = (dataSearch, element, item, flagValid) => {
  const timeData = item.date !== null && item.date !== '' ? dayjs(item.date).toDate() : null;
  const timeSearch = dayjs(dataSearch.advance[element]).toDate();

  if (dataSearch.advance[element] !== null && timeData !== null && timeData > timeSearch) {
    flagValid = false;
  }

  return flagValid;
};

// Filter score
// Params:
//   @dataSearch: Data search
//   @element: Key name
//   @item: Data of candidate
//   @flagValid: Flag item valid with filter
// Output:
//   return: Flag of item
const filterScore = (dataSearch, element, item, flagValid) => {
  if (dataSearch.advance[element] !== '' && parseInt(item[element], 10) < parseInt(dataSearch.advance[element], 10)) {
    flagValid = false;
  }

  return flagValid;
};

/**
 * Handle search item in array
 *
 * @param string searchKey
 * @param array<object> items
 * @returns array<object> List item
 */
const searchItems = (dataSearch, items) => {
  const dataClone = cloneDeep(dataSearch);
  const search = normalizeCharacter(dataClone.search_key);
  return items.filter((item) => {
    let flagValid = false;
    // Filter by search_key
    Object.entries(item).forEach((value) => {
      if (COLUMN_SEARCH.includes(value[0]) && normalizeCharacter(value[1]).includes(search)) {
        flagValid = true;
      }
    });

    // Filter by condition advance
    if (flagValid && 'advance' in dataClone) {
      Object.keys(dataClone.advance).forEach((element) => {
        // Date interview must > search date
        if (element.includes('date_interview_from')) {
          flagValid = filterInterviewDateFrom(dataClone, element, item, flagValid);
        // Date interview must < search date
        } else if (element.includes('date_interview_to')) {
          flagValid = filterInterviewDateTo(dataClone, element, item, flagValid);
        // Score must > search score
        } else if (element.includes('score')) {
          flagValid = filterScore(dataClone, element, item, flagValid);
        } else if (dataClone.advance[element] !== '' && item[element] !== dataClone.advance[element]) {
          flagValid = false;
        }
      });
    }
    return flagValid;
  });
};

// Set data of file function
// Params:
//  @file: file
//  @readFileResult: result after reading the file
// Return: object data file
const setDataFile = (file, readFileResult) => {
  const dataFile = {
    size: '',
    ext: '',
    name: '',
    filename: '',
    preview: '',
  };
  dataFile.preview = readFileResult;
  dataFile.size = file.size.toString();
  dataFile.filename = file.name;
  const arrFileExt = file.name.toString().split('.');
  dataFile.ext = arrFileExt[arrFileExt.length - 1].toString();
  const ind = dataFile.preview.search(',');
  dataFile.name = dataFile.preview.slice(ind + 1);
  return dataFile;
};

// Convert string to time function
const convertToTime = (time) => {
  // Replace ':' to ''
  let timeClone = time.replaceAll(':', '');
  const patternTime = /^([01]\d|2[0-3]):([0-5]\d)$/;
  const hourClone = timeClone.substring(0, 2).padStart(2, '0');
  const minuteClone = timeClone.substring(2, 4).padEnd(2, '0');
  // Get 4 first character of string to set time
  const resultTime = `${hourClone}:${minuteClone}`;
  // Check pattern
  if (patternTime.test(resultTime)) {
    timeClone = resultTime;
  } else {
    timeClone = '12:00';
  }

  return timeClone;
};

// Check evaluate
const checkEvaluate = (interviewer) => {
  let evaluateFailed = false;
  let notEvaluate = false;
  interviewer.forEach((item) => {
    if (item.evaluate === EVALUATE.NOT_INTERVIEW_YET) {
      notEvaluate = true;
    } else if (item.evaluate === EVALUATE.FAILED) {
      evaluateFailed = true;
    }
  });
  return {
    flagEvaluteFailed: evaluateFailed,
    flagNotEvaluate: notEvaluate,
  };
};

// Preview file
const previewCV = (linkCV) => {
  if (linkCV.includes('.docx') || linkCV.includes('.doc')) {
    return `https://view.officeapps.live.com/op/view.aspx?src=${linkCV}`;
  }
  return linkCV;
};

export {
  searchItems,
  setDataFile,
  convertToTime,
  checkEvaluate,
  previewCV,
};
