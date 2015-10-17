import React from 'react';
import FRC from 'formsy-react-components';
import DropzoneComponent from 'react-dropzone-component';
import request from 'superagent';
import Promise from 'promise';

Formsy.addValidationRule('notUploading', function(values, value) {
  return !value;
})

var FormsyDropzoneComponent = React.createClass({
  componentConfig: {
    allowedFiletypes: ['.mov'],
    showFiletypeIcon: true,
    postUrl: '/upload-video-to-s3'
  },
  djsConfig: {
    acceptedFiles: 'video/*',
    maxFiles: 1,
    dictDefaultMessage: 'Click to upload or drag a file here'
  },
  mixins: [Formsy.Mixin],
  render: function () {
    var eventHandlers = {
      addedfile: function() { this.props.onFileAdded() }.bind(this),
      success: function(file, res, xhr ){
        this.props.onFileUploadSuccess(res.video_id);
      }.bind(this),
      complete: function() { this.props.onFileUploadComplete() }.bind(this)
    };
    return (
      <div>
        <DropzoneComponent 
          config={this.componentConfig} 
          djsConfig={this.djsConfig} 
          eventHandlers={eventHandlers}
        />
      </div>
    );
  }
});

export class LiftForm extends React.Component {
  constructor() {
    super();
    this.state = {canSubmit: false, videoId: '', isUploading: false};
  }
  onFileAdded() {
    this.setState({isUploading: true});
  }
  onFileUploadSuccess(videoId) {
    this.setState({videoId: videoId});
  }
  onFileUploadComplete(){
    this.setState({isUploading: false});
  }
  enableButton() {
    this.setState({canSubmit: true});
  }
  disableButton() {
    this.setState({canSubmit: false});
  }
  submit(form) {
    let promise = new Promise(
      function(resolve, reject) {
        let data = {
          "name": form.name,
          "reps": form.reps,
          "weight": form.weight
        };
        if (this.state.videoId) data.video_id = this.state.videoId;
        request
          .post(__APIURL__.concat('/api/lift'))
          .send(data)
          .end(function(err,res){
            // this should be in res.body, superagent :(
            err ? reject(err) : resolve(JSON.parse(res.text));
          });
        }.bind(this)
    );
    promise.then(
      function(lift) {
        if(form.text) {
          const data = {
            "text": form.text,
            "lift_id": lift.id
          }
          request
            .post(__APIURL__.concat('/api/comment'))
            .send(data)
            .end(function(err,res){
              err ? reject(err) : window.location.replace(__APIURL__);
            });
        } else {
          window.location.replace(__APIURL__);
        }

      }
    ).catch(
      function(err) {
        alert(err);
        console.error(err);
      }
    );
  }
  render() {
    const names = [
      {value: '', label: 'Please select…'},
      {value: 'squat', label: 'Squat'},
      {value: 'bench', label: 'Bench'},
      {value: 'deadlift', label: 'Deadlift'}  
    ];
    
    return (
      <div>
        <h3>Add a lift</h3>
        <hr/>
        <Formsy.Form 
          onValidSubmit={this.submit.bind(this)} 
          onValid={this.enableButton.bind(this)} 
          onInvalid={this.disableButton.bind(this)}
        >
          <FRC.Select name="name" label="Lift" options={names} required />
          <FRC.Input name="weight" label="Weight" type="text" required />
          <FRC.Input name="reps" label="Reps" type="text" required />
          <FRC.Row layout="horizontal" label="Video (optional)">
            <FormsyDropzoneComponent
              name="this-is-required"
              validations="notUploading" 
              value={this.state.isUploading}
              onFileAdded={this.onFileAdded.bind(this)}
              onFileUploadSuccess={this.onFileUploadSuccess.bind(this)}
              onFileUploadComplete={this.onFileUploadComplete.bind(this)}
            />
          </FRC.Row>
          <FRC.Textarea name="text" label="Comment (optional)" rows={3} cols={40} />
          <FRC.Row layout={this.state.layout}>
            <input 
              className="btn btn-primary" 
              disabled={!this.state.canSubmit} 
              formNoValidate={true} 
              type="submit" 
              defaultValue="Submit" 
            />
          </FRC.Row>
        </Formsy.Form>
      </div>
    );
  }
}
