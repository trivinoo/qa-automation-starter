describe('QA Automation Playground - Cypress Test Suite', () => {
  const baseUrl = 'http://127.0.0.1:8000';

  beforeEach(() => {
    // Navigate to the Web App Under Test
    cy.visit(baseUrl);
  });

  it('Scenario 1: Loads the home page and product list properly', () => {
    // Assert page header
    cy.contains('h1', 'QA Playground - System Under Test (SUT)').should('be.visible');

    // Assert product table has items
    cy.get('[data-testid="products-table"]').should('exist');
    cy.get('#table-body tr').should('have.length.at.least', 1);
  });

  it('Scenario 2: Successfully logs in with valid credentials', () => {
    // Type credentials using data-testid attributes (best QA practice)
    cy.get('[data-testid="username-input"]').type('student@test.com');
    cy.get('[data-testid="password-input"]').type('Password123!');

    // Click the submit button
    cy.get('[data-testid="login-button"]').click();

    // Assert UI feedback
    cy.get('[data-testid="status-message"]')
      .should('be.visible')
      .and('contain.text', 'Login successful! Welcome, QA Student')
      .and('have.class', 'success');
  });

  it('Scenario 3: Displays error message when credentials are invalid', () => {
    cy.get('[data-testid="username-input"]').type('student@test.com');
    cy.get('[data-testid="password-input"]').type('WrongPassword');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="status-message"]')
      .should('be.visible')
      .and('contain.text', 'Invalid credentials')
      .and('have.class', 'error');
  });
});
