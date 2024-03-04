import { ref } from 'vue';
import ajv from 'boot/ajv';

export default function useValidate() {
  const errors = ref({});
  const validate = (schema, data) => {
    errors.value = {};
    const validateFn = ajv.compile(schema);
    const valid = validateFn(data);
    if (validateFn.errors) {
      const lst = {};
      validateFn.errors.forEach((obj) => {
        const dataPath = obj.instancePath
          .slice(1, obj.instancePath.length);
        if (!lst[dataPath]) {
          lst[dataPath] = obj.message;
        }
      });
      errors.value = lst;
    }

    return valid;
  };

  return {
    errors,
    // methods
    validate,
  };
}
