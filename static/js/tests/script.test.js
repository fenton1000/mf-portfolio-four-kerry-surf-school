/**
 * @jest-environment jsdom
 */

const $ = require('jquery');

Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(), // Deprecated
      removeListener: jest.fn(), // Deprecated
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
  
const changeHomeView = require('../script');

beforeAll(() => {
    document.body.innerHTML = '<div id="accordion"></div>';
    Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 500,
      });
    changeHomeView();
});

describe('home page responsiveness scripts run for width less than 650px', () => {
    test('expect accordion to have make-div-appear class', () => {
        const accordion = document.getElementById('accordion');
        expect(accordion.getAttribute('class')).toEqual('make-div-appear');
    });
});