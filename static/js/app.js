// Custom JavaScript for Inventory System
(function () {
  function getValidationMessage(field) {
    const value = field.value.trim();
    const min = field.getAttribute('min');
    const type = field.getAttribute('type');

    if (field.hasAttribute('required') && !value) {
      return field.dataset.requiredMessage || 'This field is required';
    }

    if (type === 'number' && value) {
      const numberValue = Number(value);

      if (Number.isNaN(numberValue)) {
        return field.dataset.invalidMessage || 'Enter a valid value';
      }

      if (min !== null && numberValue < Number(min)) {
        return field.dataset.rangeMessage || 'Enter a valid value';
      }
    }

    return '';
  }

  function setFieldError(field, message) {
    const feedback = field.parentElement.querySelector('.invalid-feedback');
    field.classList.toggle('is-invalid', Boolean(message));

    if (feedback) {
      feedback.textContent = message;
      if (message) {
        feedback.classList.remove('hidden');
      } else {
        feedback.classList.add('hidden');
      }
    }
  }

  function validateField(field) {
    const message = getValidationMessage(field);
    setFieldError(field, message);
    return !message;
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[data-custom-validation]').forEach(function (form) {
      const fields = form.querySelectorAll('input, select, textarea');

      fields.forEach(function (field) {
        ['input', 'change', 'blur'].forEach(function (eventName) {
          field.addEventListener(eventName, function () {
            validateField(field);
          });
        });
      });

      form.addEventListener('submit', function (event) {
        let firstInvalidField = null;

        fields.forEach(function (field) {
          const isValid = validateField(field);
          if (!isValid && !firstInvalidField) {
            firstInvalidField = field;
          }
        });

        if (firstInvalidField) {
          event.preventDefault();
          firstInvalidField.focus();
        }
      });
    });
  });
})();
