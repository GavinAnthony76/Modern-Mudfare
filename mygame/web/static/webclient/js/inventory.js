/**
 * Inventory System - Manage items and equipment
 */

class Inventory {
  constructor(maxSize = 20) {
    this.items = [];
    this.maxSize = maxSize;
  }

  addItem(item) {
    if (this.items.length >= this.maxSize) return false;
    this.items.push(item);
    return true;
  }

  removeItem(itemId) {
    const index = this.items.findIndex(item => item.id === itemId);
    if (index !== -1) {
      this.items.splice(index, 1);
      return true;
    }
    return false;
  }

  findItem(itemId) {
    return this.items.find(item => item.id === itemId);
  }

  useItem(itemId) {
    const item = this.findItem(itemId);
    if (!item) return false;

    if (item.type === 'consumable') {
      this.removeItem(itemId);
      return true;
    }

    return false;
  }

  getInventoryCount() {
    return this.items.length;
  }

  isFull() {
    return this.items.length >= this.maxSize;
  }

  clear() {
    this.items = [];
  }

  serialize() {
    return this.items;
  }

  static deserialize(data) {
    const inv = new Inventory();
    inv.items = data || [];
    return inv;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Inventory;
}
