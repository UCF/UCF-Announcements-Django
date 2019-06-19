function confirmNewUser() {
  const $urlInput = $('#confirmUserURL');
  const url = $urlInput.val();
  const $token = $('input[name="csrfmiddlewaretoken"]');

  $.post(
    url,
    {
      csrfmiddlewaretoken: $token.val()
    }
  );
}

function showNewUserModal($) {
  const $hfShowModal = $('#showNewUserModal');
  const $newUserModal = $('#newUserModal');
  const showModal = $hfShowModal ? $hfShowModal.val() : false;

  if (showModal === 'True') {
    $newUserModal.modal();
  }

  $newUserModal.on('hide.bs.modal', confirmNewUser);
}

function initDatepickers($) {
  const testDate = document.createElement('input');
  testDate.type = 'date';

  if (testDate.type === 'text') {
    $('.date-picker').datepicker({
      dateFormat: 'yy-mm-dd'
    });
  }
}

function initMaskedInput($) {
  $('.phone-number').mask('(999) 999-9999');
}

if (jQuery !== 'undefined') {
  jQuery(document).ready(($) => {
    showNewUserModal($);
    initDatepickers($);
    initMaskedInput($);
  });
}
