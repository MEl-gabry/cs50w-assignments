document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email("", "", ""));

  // By default, load the inbox
  load_mailbox('inbox');
});

function get_date() {
  const current_date = new Date();
  let months = new Map();
  months.set(0, 'Jan');
  months.set(1, "Feb");
  months.set(2, "Mar");
  months.set(3, "Apr");
  months.set(4, "May");
  months.set(5, "Jun");
  months.set(6, "Jul");
  months.set(7, "Aug");
  months.set(8, "Sep");
  months.set(9, "Oct");
  months.set(10, "Nov");
  months.set(11, "Dec");
  let month = months.get(current_date.getMonth());
  let date = current_date.getDate();
  let year = current_date.getFullYear();
  let hour = current_date.getHours();
  let period = "";
  if (hour >= 0 && hour < 12) {
    period = "AM";
    if (hour == 0) {
      hour = 12;
    }
  }
  else if (hour >= 12) {
    period = "PM";
    hour -= 12;
  }
  let minutes = current_date.getMinutes();
  if (minutes < 10) {
    minutes = `0${minutes}`;
  }
  const time = month + " " + date + " " + year + ", " + hour + ":" + minutes + " " + period;
  return time;
}

function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'block';
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#timestamp').innerHTML = email.timestamp;
    document.querySelector('#sender').innerHTML = `From: ${email.sender}`;
    document.querySelector('#recipients').innerHTML = `To: ${email.recipients}`;
    document.querySelector('#subject').innerHTML = email.subject;
    document.querySelector('#body').innerHTML = email.body;
    document.querySelector('#reply').addEventListener('click', () => {
      let subject = email.subject;
      if (!subject.includes("Re:")) {
        subject = `Re: ${subject}`;
      }
      const time = get_date();
      const user_email = document.querySelector('#user_email').innerHTML;
      const body = `On ${time} ${user_email} wrote:`;
      compose_email(email.sender, subject, body);
    });
  });
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}

function compose_email(recipient, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

  form = document.querySelector('#compose-form');
  form.onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });
    load_mailbox('sent');

    return false;
  }
}

function load_mailbox(mailbox) {
  
  const email_view = document.querySelector('#emails-view');

  // Show the mailbox and hide other views
  email_view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'none';

  // Show the mailbox name
  email_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  let archive = false;
  let archive_text = "";
  
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    const ul = document.createElement('ul');
    ul.classList.add('list-group');
    email_view.appendChild(ul);
    emails.forEach(email => {
      const li = document.createElement("li");
      const sender = document.createElement("p");
      const subject = document.createElement("p");
      const timestamp = document.createElement("p");
      sender.innerHTML = email.sender;
      subject.innerHTML = email.subject;
      timestamp.innerHTML = email.timestamp;
      li.classList.add('list-group-item');
      if (email.read === true) {
        li.classList.add('list-group-item-dark');
      }
      li.id = email.id;

      ul.appendChild(li);
      li.appendChild(sender);
      li.appendChild(subject);
      li.appendChild(timestamp);
      
      if (mailbox === "inbox") {
        archive = true;
        archive_text = "Archive";
      } 
      else if (mailbox === "archive") {
        archive = false;
        archive_text = "Unarchive";
      }
      if (archive_text != "") {
        const archive_button = document.createElement("button");
        archive_button.classList.add('btn');
        archive_button.classList.add('btn-primary');
        archive_button.innerHTML = archive_text;
        archive_button.id = email.id;
        li.appendChild(archive_button);
      }
    });
  });
  
  email_view.addEventListener('click', element => {
    if (element.target.className.includes('list-group-item')) {
      view_email(element.target.id);
    }
    else if (element.target.tagName === "BUTTON") {
      fetch(`/emails/${element.target.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: archive
        })
      });
      setTimeout(() => {
        location.reload();
      }, 1);
    }
  });
}