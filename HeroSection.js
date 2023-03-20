import React from 'react';
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

export default function HeroSection() {
  return (
    <div className='hero-container'>
      <video src='/videos/video-2.mp4' autoPlay loop muted />
      <h1>BEGIN YOUR INVESTMENT JOURNEY HERE</h1>
      <p>Make informed decisions with your money</p>
      <div className='hero-btns'>
          <Button 
          className='btns'
          buttonStyle='btn--outline'
          buttonSize='btn--large'>
              GET STARTED
            </Button>
        <Button 
          className='btns'
          buttonStyle='btn--primary'
          buttonSize='btn--large'>
              Watch <i className='far fa-play-circle' />
            </Button>
      </div>
    </div>
  )
}
