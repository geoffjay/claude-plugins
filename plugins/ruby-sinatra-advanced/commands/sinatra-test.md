---
description: Generate comprehensive tests for Sinatra routes, middleware, and helpers using RSpec or Minitest
---

# Sinatra Test Command

Generates comprehensive test suites for Sinatra applications including route tests, middleware tests, helper tests, and integration tests using RSpec or Minitest.

## Arguments

- **$1: test-type** (optional) - Type of tests to generate: `routes`, `middleware`, `helpers`, or `all` (default: `all`)
- **$2: framework** (optional) - Testing framework: `rspec` or `minitest` (default: `rspec`)

## Usage Examples

```bash
# Generate all tests using RSpec
/sinatra-test

# Generate only route tests with RSpec
/sinatra-test routes

# Generate all tests using Minitest
/sinatra-test all minitest

# Generate middleware tests with Minitest
/sinatra-test middleware minitest

# Generate helper tests with RSpec
/sinatra-test helpers rspec
```

## Workflow

### Step 1: Analyze Application Structure

**Discovery Phase:**

1. Identify application type (classic vs modular)
2. Locate controller files
3. Extract route definitions
4. Find middleware stack
5. Identify helper methods
6. Check existing test structure
7. Detect testing framework if already configured

**Files to Analyze:**
```ruby
# Controllers
app/controllers/**/*.rb
app.rb (classic style)

# Middleware
config.ru
config/**/*.rb

# Helpers
app/helpers/**/*.rb
helpers/ directory

# Existing tests
spec/**/*_spec.rb
test/**/*_test.rb
```

**Route Extraction:**
```ruby
# Parse routes from controller files
# Identify: HTTP method, path, parameters, conditions

# Example routes to extract:
get '/users' do
  # Handler
end

get '/users/:id', :id => /\d+/ do
  # Handler with constraint
end

post '/users', :provides => [:json] do
  # Handler with content negotiation
end
```

### Step 2: Generate Test Structure (RSpec)

**Create spec_helper.rb if missing:**

```ruby
# spec/spec_helper.rb
ENV['RACK_ENV'] = 'test'

require 'simplecov'
SimpleCov.start do
  add_filter '/spec/'
  add_filter '/config/'
end

require_relative '../config/environment'
require 'rack/test'
require 'rspec'
require 'json'

# Database setup (if applicable)
if defined?(Sequel)
  require 'database_cleaner/sequel'

  RSpec.configure do |config|
    config.before(:suite) do
      DatabaseCleaner.strategy = :transaction
      DatabaseCleaner.clean_with(:truncation)
    end

    config.around(:each) do |example|
      DatabaseCleaner.cleaning do
        example.run
      end
    end
  end
end

RSpec.configure do |config|
  config.include Rack::Test::Methods

  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
  config.filter_run_when_matching :focus
  config.example_status_persistence_file_path = 'spec/examples.txt'
  config.disable_monkey_patching!
  config.warnings = true
  config.order = :random
  Kernel.srand config.seed
end

# Helper methods for all specs
module SpecHelpers
  def json_response
    JSON.parse(last_response.body)
  end

  def auth_header(token)
    { 'HTTP_AUTHORIZATION' => "Bearer #{token}" }
  end
end

RSpec.configure do |config|
  config.include SpecHelpers
end
```

**Create support files:**

```ruby
# spec/support/factory_helper.rb (if using factories)
require 'factory_bot'

RSpec.configure do |config|
  config.include FactoryBot::Syntax::Methods
end

# spec/support/shared_examples.rb
RSpec.shared_examples 'authenticated endpoint' do
  it 'returns 401 without authentication' do
    send(http_method, path)
    expect(last_response.status).to eq(401)
  end
end

RSpec.shared_examples 'json endpoint' do
  it 'returns JSON content type' do
    send(http_method, path, valid_params)
    expect(last_response.content_type).to include('application/json')
  end
end
```

### Step 3: Generate Route Tests

**For each route, generate comprehensive tests:**

```ruby
# spec/controllers/users_controller_spec.rb
require_relative '../spec_helper'

RSpec.describe UsersController do
  def app
    UsersController
  end

  describe 'GET /users' do
    context 'with no users' do
      it 'returns empty array' do
        get '/users'
        expect(last_response).to be_ok
        expect(json_response).to eq([])
      end
    end

    context 'with existing users' do
      let!(:users) { create_list(:user, 3) }

      it 'returns all users' do
        get '/users'
        expect(last_response).to be_ok
        expect(json_response.length).to eq(3)
      end

      it 'includes user attributes' do
        get '/users'
        user_data = json_response.first
        expect(user_data).to have_key('id')
        expect(user_data).to have_key('name')
        expect(user_data).to have_key('email')
      end
    end

    context 'with pagination' do
      let!(:users) { create_list(:user, 25) }

      it 'respects page parameter' do
        get '/users?page=2&per_page=10'
        expect(json_response.length).to eq(10)
      end

      it 'includes pagination metadata' do
        get '/users?page=1&per_page=10'
        expect(json_response['meta']).to include(
          'total' => 25,
          'page' => 1,
          'per_page' => 10
        )
      end
    end

    context 'with filtering' do
      let!(:active_user) { create(:user, active: true) }
      let!(:inactive_user) { create(:user, active: false) }

      it 'filters by active status' do
        get '/users?active=true'
        expect(json_response.length).to eq(1)
        expect(json_response.first['id']).to eq(active_user.id)
      end
    end
  end

  describe 'GET /users/:id' do
    let(:user) { create(:user) }

    context 'when user exists' do
      it 'returns user details' do
        get "/users/#{user.id}"
        expect(last_response).to be_ok
        expect(json_response['id']).to eq(user.id)
      end

      it 'includes all user attributes' do
        get "/users/#{user.id}"
        expect(json_response).to include(
          'id' => user.id,
          'name' => user.name,
          'email' => user.email
        )
      end
    end

    context 'when user does not exist' do
      it 'returns 404' do
        get '/users/99999'
        expect(last_response.status).to eq(404)
      end

      it 'returns error message' do
        get '/users/99999'
        expect(json_response).to include('error')
      end
    end

    context 'with invalid id format' do
      it 'returns 404' do
        get '/users/invalid'
        expect(last_response.status).to eq(404)
      end
    end
  end

  describe 'POST /users' do
    let(:valid_attributes) do
      {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'SecurePass123'
      }
    end

    context 'with valid attributes' do
      it 'creates a new user' do
        expect {
          post '/users', valid_attributes.to_json,
            'CONTENT_TYPE' => 'application/json'
        }.to change(User, :count).by(1)
      end

      it 'returns 201 status' do
        post '/users', valid_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq(201)
      end

      it 'returns created user' do
        post '/users', valid_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(json_response).to include(
          'name' => 'John Doe',
          'email' => 'john@example.com'
        )
      end

      it 'does not return password' do
        post '/users', valid_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(json_response).not_to have_key('password')
      end
    end

    context 'with invalid attributes' do
      it 'returns 422 status' do
        post '/users', { name: '' }.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq(422)
      end

      it 'returns validation errors' do
        post '/users', { name: '' }.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(json_response).to have_key('errors')
      end

      it 'does not create user' do
        expect {
          post '/users', { name: '' }.to_json,
            'CONTENT_TYPE' => 'application/json'
        }.not_to change(User, :count)
      end
    end

    context 'with duplicate email' do
      let!(:existing_user) { create(:user, email: 'john@example.com') }

      it 'returns 422 status' do
        post '/users', valid_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq(422)
      end

      it 'returns uniqueness error' do
        post '/users', valid_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(json_response['errors']).to include('email')
      end
    end
  end

  describe 'PUT /users/:id' do
    let(:user) { create(:user) }
    let(:update_attributes) { { name: 'Updated Name' } }

    context 'when user exists' do
      it 'updates user attributes' do
        put "/users/#{user.id}", update_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        user.reload
        expect(user.name).to eq('Updated Name')
      end

      it 'returns 200 status' do
        put "/users/#{user.id}", update_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(last_response).to be_ok
      end

      it 'returns updated user' do
        put "/users/#{user.id}", update_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(json_response['name']).to eq('Updated Name')
      end
    end

    context 'with invalid attributes' do
      it 'returns 422 status' do
        put "/users/#{user.id}", { email: 'invalid' }.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq(422)
      end

      it 'does not update user' do
        original_email = user.email
        put "/users/#{user.id}", { email: 'invalid' }.to_json,
          'CONTENT_TYPE' => 'application/json'
        user.reload
        expect(user.email).to eq(original_email)
      end
    end

    context 'when user does not exist' do
      it 'returns 404' do
        put '/users/99999', update_attributes.to_json,
          'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq(404)
      end
    end
  end

  describe 'DELETE /users/:id' do
    let!(:user) { create(:user) }

    context 'when user exists' do
      it 'deletes the user' do
        expect {
          delete "/users/#{user.id}"
        }.to change(User, :count).by(-1)
      end

      it 'returns 204 status' do
        delete "/users/#{user.id}"
        expect(last_response.status).to eq(204)
      end

      it 'returns empty body' do
        delete "/users/#{user.id}"
        expect(last_response.body).to be_empty
      end
    end

    context 'when user does not exist' do
      it 'returns 404' do
        delete '/users/99999'
        expect(last_response.status).to eq(404)
      end
    end
  end

  # Authentication tests
  describe 'authentication' do
    let(:protected_path) { '/users' }
    let(:http_method) { :get }
    let(:path) { protected_path }

    it_behaves_like 'authenticated endpoint'
  end

  # Content negotiation tests
  describe 'content negotiation' do
    let(:user) { create(:user) }

    context 'with Accept: application/json' do
      it 'returns JSON' do
        get "/users/#{user.id}", {}, { 'HTTP_ACCEPT' => 'application/json' }
        expect(last_response.content_type).to include('application/json')
      end
    end

    context 'with Accept: application/xml' do
      it 'returns XML' do
        get "/users/#{user.id}", {}, { 'HTTP_ACCEPT' => 'application/xml' }
        expect(last_response.content_type).to include('application/xml')
      end
    end
  end
end
```

### Step 4: Generate Middleware Tests

```ruby
# spec/middleware/custom_middleware_spec.rb
require_relative '../spec_helper'

RSpec.describe CustomMiddleware do
  let(:app) { ->(env) { [200, {}, ['OK']] } }
  let(:middleware) { CustomMiddleware.new(app) }
  let(:request) { Rack::MockRequest.new(middleware) }

  describe 'request processing' do
    it 'passes request to next middleware' do
      response = request.get('/')
      expect(response.status).to eq(200)
    end

    it 'adds custom header to response' do
      response = request.get('/')
      expect(response.headers['X-Custom-Header']).to eq('value')
    end

    it 'modifies request environment' do
      env = {}
      middleware.call(env)
      expect(env['custom.key']).to be_present
    end
  end

  describe 'error handling' do
    let(:app) { ->(env) { raise StandardError, 'Error' } }

    it 'catches errors from downstream' do
      response = request.get('/')
      expect(response.status).to eq(500)
    end

    it 'logs error' do
      expect { request.get('/') }.to change { error_log.size }.by(1)
    end
  end

  describe 'configuration' do
    let(:middleware) { CustomMiddleware.new(app, option: 'value') }

    it 'accepts configuration options' do
      expect(middleware.options[:option]).to eq('value')
    end

    it 'applies configuration to behavior' do
      response = request.get('/')
      expect(response.headers['X-Option']).to eq('value')
    end
  end
end
```

### Step 5: Generate Helper Tests

```ruby
# spec/helpers/application_helpers_spec.rb
require_relative '../spec_helper'

RSpec.describe ApplicationHelpers do
  let(:dummy_class) do
    Class.new do
      include ApplicationHelpers

      # Mock request/session for helper context
      def request
        @request ||= Struct.new(:path_info).new('/test')
      end

      def session
        @session ||= {}
      end
    end
  end

  let(:helpers) { dummy_class.new }

  describe '#current_user' do
    context 'when user is logged in' do
      before do
        helpers.session[:user_id] = 1
        allow(User).to receive(:find).with(1).and_return(
          double('User', id: 1, name: 'John')
        )
      end

      it 'returns current user' do
        expect(helpers.current_user).to be_present
        expect(helpers.current_user.id).to eq(1)
      end

      it 'memoizes user' do
        expect(User).to receive(:find).once
        helpers.current_user
        helpers.current_user
      end
    end

    context 'when user is not logged in' do
      it 'returns nil' do
        expect(helpers.current_user).to be_nil
      end
    end
  end

  describe '#logged_in?' do
    it 'returns true when current_user exists' do
      allow(helpers).to receive(:current_user).and_return(double('User'))
      expect(helpers.logged_in?).to be true
    end

    it 'returns false when current_user is nil' do
      allow(helpers).to receive(:current_user).and_return(nil)
      expect(helpers.logged_in?).to be false
    end
  end

  describe '#format_date' do
    let(:date) { Time.new(2024, 1, 15, 10, 30, 0) }

    it 'formats date with default format' do
      expect(helpers.format_date(date)).to eq('2024-01-15')
    end

    it 'accepts custom format' do
      expect(helpers.format_date(date, '%m/%d/%Y')).to eq('01/15/2024')
    end

    it 'handles nil date' do
      expect(helpers.format_date(nil)).to eq('')
    end
  end

  describe '#truncate' do
    let(:long_text) { 'This is a very long text that should be truncated' }

    it 'truncates text to specified length' do
      expect(helpers.truncate(long_text, 20)).to eq('This is a very long...')
    end

    it 'does not truncate short text' do
      short_text = 'Short'
      expect(helpers.truncate(short_text, 20)).to eq('Short')
    end

    it 'accepts custom omission' do
      expect(helpers.truncate(long_text, 20, omission: '…')).to include('…')
    end
  end
end
```

### Step 6: Generate Minitest Tests (Alternative)

**If framework is Minitest:**

```ruby
# test/test_helper.rb
ENV['RACK_ENV'] = 'test'

require 'simplecov'
SimpleCov.start

require_relative '../config/environment'
require 'minitest/autorun'
require 'minitest/spec'
require 'rack/test'

class Minitest::Spec
  include Rack::Test::Methods

  def json_response
    JSON.parse(last_response.body)
  end
end

# test/controllers/users_controller_test.rb
require_relative '../test_helper'

describe UsersController do
  def app
    UsersController
  end

  describe 'GET /users' do
    it 'returns success' do
      get '/users'
      assert last_response.ok?
    end

    it 'returns JSON' do
      get '/users'
      assert_includes last_response.content_type, 'application/json'
    end

    describe 'with existing users' do
      before do
        @users = 3.times.map { User.create(name: 'Test') }
      end

      it 'returns all users' do
        get '/users'
        assert_equal 3, json_response.length
      end
    end
  end

  describe 'POST /users' do
    let(:valid_params) { { name: 'John', email: 'john@example.com' } }

    it 'creates user' do
      assert_difference 'User.count', 1 do
        post '/users', valid_params.to_json,
          'CONTENT_TYPE' => 'application/json'
      end
    end

    it 'returns 201' do
      post '/users', valid_params.to_json,
        'CONTENT_TYPE' => 'application/json'
      assert_equal 201, last_response.status
    end
  end
end
```

### Step 7: Generate Integration Tests

```ruby
# spec/integration/user_registration_spec.rb
require_relative '../spec_helper'

RSpec.describe 'User Registration Flow' do
  def app
    Sinatra::Application
  end

  describe 'complete registration process' do
    let(:user_params) do
      {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'SecurePass123'
      }
    end

    it 'allows new user to register and log in' do
      # Step 1: Register
      post '/register', user_params.to_json,
        'CONTENT_TYPE' => 'application/json'
      expect(last_response.status).to eq(201)

      user_id = json_response['id']

      # Step 2: Verify email confirmation sent
      expect(EmailService.last_email[:to]).to eq('john@example.com')

      # Step 3: Confirm email
      token = EmailService.last_email[:token]
      get "/confirm/#{token}"
      expect(last_response.status).to eq(200)

      # Step 4: Log in
      post '/login', { email: 'john@example.com', password: 'SecurePass123' }.to_json,
        'CONTENT_TYPE' => 'application/json'
      expect(last_response.status).to eq(200)
      expect(json_response).to have_key('token')

      # Step 5: Access protected resource
      token = json_response['token']
      get '/profile', {}, auth_header(token)
      expect(last_response).to be_ok
      expect(json_response['id']).to eq(user_id)
    end
  end
end
```

### Step 8: Create Test Documentation

**Generate test README:**

```markdown
# Test Suite Documentation

## Running Tests

### All Tests
```bash
bundle exec rspec
```

### Specific Test File
```bash
bundle exec rspec spec/controllers/users_controller_spec.rb
```

### By Tag
```bash
bundle exec rspec --tag focus
```

## Test Structure

- `spec/controllers/` - Route and controller tests
- `spec/middleware/` - Middleware tests
- `spec/helpers/` - Helper method tests
- `spec/models/` - Model tests (if applicable)
- `spec/integration/` - End-to-end integration tests
- `spec/support/` - Shared examples and helpers

## Coverage

Run tests with coverage report:
```bash
COVERAGE=true bundle exec rspec
```

View coverage report:
```bash
open coverage/index.html
```

## Testing Patterns

### Route Testing
- Test successful responses
- Test error cases (404, 422, 500)
- Test authentication/authorization
- Test parameter validation
- Test content negotiation

### Helper Testing
- Test with various inputs
- Test edge cases
- Test nil handling
- Mock dependencies

### Integration Testing
- Test complete user flows
- Test interactions between components
- Test external service integration
```

## Output

**Generated files report:**
```
Test Generation Complete!

Framework: RSpec
Test Type: all

Generated Files:
  ✓ spec/spec_helper.rb
  ✓ spec/support/factory_helper.rb
  ✓ spec/support/shared_examples.rb
  ✓ spec/controllers/users_controller_spec.rb (45 examples)
  ✓ spec/controllers/posts_controller_spec.rb (38 examples)
  ✓ spec/middleware/custom_middleware_spec.rb (12 examples)
  ✓ spec/helpers/application_helpers_spec.rb (15 examples)
  ✓ spec/integration/user_registration_spec.rb (5 examples)
  ✓ TEST_README.md

Total Examples: 115
Coverage Target: 90%

Run tests: bundle exec rspec
```

## Error Handling

- Handle applications without routes gracefully
- Skip already existing test files (or offer to overwrite)
- Detect testing framework from Gemfile
- Warn if test dependencies missing
- Handle parse errors in application files
