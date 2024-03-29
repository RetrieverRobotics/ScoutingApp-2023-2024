/**
 * 
 * @param {string[][]} columns 
 * @param {string[][]} mappings
 */
function parseValMap(columns, mappings) {
  //list of rows, but only one row
  const cols = columns[0];
  const maps = mappings[0];

  const valMap = {};
  for (let i = 0; i < cols.length; i++) {
    const columnName = cols[i].trim();
    const mapCode = maps[i].trim();
    if (mapCode.length == 0) continue;
    valMap[columnName] = eval(mapCode);
  }
  return valMap;
}

/**
 * @param {string} sortBy The column to sort by. (!ID COLUMN)
 * @param {string} sortOrder The order to sort in. ("DESCENDING" | "ASCENDING")
 * @param {string} compressMethod The method to use when compressing rows into one value per column. ("AVG" | "MAX" | "MIN")
 * @param {string} idColumnName
 * @param {string} limitColumnName
 * @param {string|object} limitMin Set bottom of the limit. ("-" | value)
 * @param {string|object} limitMax Set top of the limit.   ("+" | value)
 * @param {string[][]} mapping
 */
function sortUI(sortBy, sortOrder, compressMethod, idColumnName, limitColumnName, limitMin, limitMax, rows, columns, mapping) {
  const valMap = parseValMap(columns, mapping);
  const idColumn = columns[0].indexOf(idColumnName);
  let sortColumn = columns[0].indexOf(sortBy);
  if (sortColumn == -1) return `Cannot sort by ${sortBy} column.`;
  else if (sortColumn == idColumn) return "Cannot sort by ID column.";
  
  if (sortColumn > idColumn) sortColumn--; //adjust for id column being removed from each value in grabbed
  
  const limited = limitRows(limitColumnName, limitMin, limitMax, rows, columns, mapping);
  
  let grabbed;
  switch (compressMethod.toUpperCase()) {
    case "AVG": grabbed = grabAvg(idColumnName, limited, columns); break;
    case "MAX": grabbed = grabMax(idColumnName, limited, columns); break;
    case "MIN": grabbed = grabMin(idColumnName, limited, columns); break;
    default:
      throw new Error(`Invalid compress method "${compressMethod}".`);
  }
  
  if (grabbed.size < 1)
    return "Nothing to sort.";

  //map to 2d array
  const unsorted = []; //object[][] {id, value}
  grabbed.forEach((value, key) => { unsorted.push([key, value[sortColumn]]) });
  
  //sort
  const sortConst = sortOrder == "ASCENDING" ? 1 : sortOrder == "DESCENDING" ? -1 : 0;
  if (unsorted.every(v => typeof v[1] == "number" || typeof v[1] == "boolean"))
    return unsorted.sort((a,b) => (a[1]-b[1])*sortConst);
  else if (sortBy in valMap) {
    const m = valMap[sortBy];
    return unsorted.sort((a,b) => (m(a[1])-m(b[1]))*sortConst);
  }
  //sort "alphabetically" (may not only be strings)
  return sortConst < 1 ? unsorted.sort() : unsorted.sort().reverse();
}

const LIMIT_MAX = "[+]";
const LIMIT_MIN = "[-]";

/**
 * @param {string} columnName Limit Column name.
 * @param {object[][]} rows
 * @param {string[][]} columns
 * @param {string[][]} mapping
 */
function getLimitRange(columnName, rows, columns, mapping) {
  const valMap = parseValMap(columns, mapping);
  const limitColumn = columns[0].indexOf(columnName);
  const unique = [];
  let rtv;

  //get unique values
  for (const row of rows) {
    const value = row[limitColumn];
    if (value !== "" && !unique.includes(value))
      unique.push(value);
  }

  if (unique.length==0) return [[LIMIT_MIN, LIMIT_MAX]];

  //sort ascending (min to max)
  if (unique.every(v => typeof v == "number" || typeof v == "boolean"))
    rtv = unique.sort((a,b)=>a-b);
  else if (columnName in valMap) {
    const m = valMap[columnName];
    rtv = unique.sort((a,b)=>m(a)-m(b));
  }
  else
    rtv = unique.sort().reverse();
  
  //add ui components "-" (least) and "+" (greatest)
  rtv.splice(0, 0, LIMIT_MIN);
  rtv.push(LIMIT_MAX);
  return [rtv];
}
