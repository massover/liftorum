import React from 'react';
import { LiftForm } from './LiftForm';

import 'dropzone/dist/min/dropzone.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import '../stylesheet.css';

var liftForm = document.getElementById('liftForm');
if (liftForm) {
  React.render(<LiftForm />, liftForm);
}

