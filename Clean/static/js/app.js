document.addEventListener("DOMContentLoaded", function() {
    // Get form elements
    const form = document.getElementById("filter-form");
    const sortBy = document.getElementById("sort_by");
    const sortOrder = document.getElementById("sort_order");
    const limit = document.getElementById("limit");
    const department = document.getElementById("category");
    const course_level = document.getElementById("course_level");
    const exclude_na = document.getElementById("exclude_na");
    const gradeRange = document.getElementById("grade-range");
    const gradeLetter = document.getElementById("grade-letter");
    const term_name = document.getElementById("term_name");
  
    // Load saved values from local storage, if available
    sortBy.value = localStorage.getItem("sortBy") || sortBy.value;
    sortOrder.value = localStorage.getItem("sortOrder") || sortOrder.value;
    limit.value = localStorage.getItem("limit") || limit.value;
    department.value = localStorage.getItem("department") || department.value;
    course_level.value = localStorage.getItem("course_level") || course_level.value;
    exclude_na.value = localStorage.getItem("exclude_na") || exclude_na.value;
    gradeRange.value = localStorage.getItem("gradeRange") || gradeRange.value;
    gradeLetter.value = localStorage.getItem("gradeLetter") || gradeLetter.value;
    term_name.value = localStorage.getItem("term_name") || term_name.value;
  
    // Save values to local storage when form is submitted
    form.addEventListener("submit", function(event) {
      localStorage.setItem("sortBy", sortBy.value);
      localStorage.setItem("sortOrder", sortOrder.value);
      localStorage.setItem("limit", limit.value);
      localStorage.setItem("department", department.value);
      localStorage.setItem("course_level", course_level.value);
      localStorage.setItem("exclude_na", exclude_na.value);
      localStorage.setItem("gradeRange", gradeRange.value);
      localStorage.setItem("gradeLetter", gradeLetter.value);
      localStorage.setItem("term_name", term_name.value);
    });
  });
  
  const gradeRange = document.getElementById("grade-range");
  const gradeRangeValue = document.getElementById("grade-range-value");
  gradeRangeValue.innerText = gradeRange.value;
  gradeRange.addEventListener("input", function() {
    gradeRangeValue.innerText = this.value;
  });
  
  const gradeLetter = document.getElementById("grade-letter");
  const gradeLetterValue = document.getElementById("grade-letter-value");
  const letterGrades = ["E", "D-", "D", "D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+"];
  gradeLetterValue.innerText = letterGrades[gradeLetter.value];
  gradeLetter.addEventListener("input", function() {
    if (this.value >= 13 || this.value == undefined) {
      gradeLetterValue.innerText = "A+";
    } else {
    gradeLetterValue.innerText = letterGrades[this.value];
    }
  });
form.addEventListener("submit", function(event) {
  event.preventDefault();
  // rest of your code
});
