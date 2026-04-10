// Task completion animation
document.addEventListener('DOMContentLoaded', function () {
  // Add smooth transitions for list items
  const listItems = document.querySelectorAll('.list-group-item');
  listItems.forEach(item => {
    item.addEventListener('mouseenter', function () {
      this.style.transition = 'all 0.3s ease';
    });
  });

  // Calendar hover effects
  const calendarDays = document.querySelectorAll('.calendar-day');
  calendarDays.forEach(day => {
    day.addEventListener('mouseenter', function () {
      if (!this.classList.contains('empty')) {
        this.style.backgroundColor = '#e7f3ff';
      }
    });

    day.addEventListener('mouseleave', function () {
      this.style.backgroundColor = '';
    });
  });

  // Form validation
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      const title = form.querySelector('input[name="title"]');
      if (title && title.value.trim() === '') {
        e.preventDefault();
        alert('Task title is required');
      }
    });
  });
});
