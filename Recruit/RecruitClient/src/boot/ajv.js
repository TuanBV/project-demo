import Ajv from 'ajv';
import ajvErrors from 'ajv-errors';
import ajvKeywords from 'ajv-keywords';
import addFormats from 'ajv-formats';
import keywords from 'keywords';

const $ajv = new Ajv({
  allErrors: true,
  removeAdditional: true,
  useDefaults: true,
  coerceTypes: true,
  $data: true,
});
// enhance the ajv instance
ajvErrors($ajv);
ajvKeywords($ajv);
addFormats($ajv);

// Add keywords
keywords.forEach((keyword) => {
  $ajv.addKeyword(keyword);
});

export default $ajv;
