const MESSAGES = {
    valueMissing: 'Por favor, preencha este campo.',
    typeMismatch: {
        email: 'Por favor, insira um endereço de e-mail válido.',
        default: 'Por favor, insira um valor válido.',
    },
    tooShort: (min) => `Por favor, use pelo menos ${min} caracteres.`,
};

function applyMessage(input) {
    const v = input.validity;
    if (v.valueMissing) {
        input.setCustomValidity(MESSAGES.valueMissing);
    } else if (v.typeMismatch) {
        input.setCustomValidity(
            MESSAGES.typeMismatch[input.type] ?? MESSAGES.typeMismatch.default
        );
    } else if (v.tooShort) {
        input.setCustomValidity(MESSAGES.tooShort(input.minLength));
    } else {
        input.setCustomValidity('');
    }
}

function setValidationMessages(input) {
    input.addEventListener('invalid', () => applyMessage(input));
    input.addEventListener('input', () => applyMessage(input));
}

document.querySelectorAll('input').forEach(setValidationMessages);
