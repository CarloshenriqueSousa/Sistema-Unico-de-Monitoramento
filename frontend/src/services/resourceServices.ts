import axios from 'axios';
import type { ResourceAllocation } from '@/types/resource';

const API_URL = import.meta.env.VITE_API_URL;

export const fetchResources = async (): Promise<ResourceAllocation[]> => {
  try {
    const response = await axios.get(`${API_URL}/resources/allocations/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching resources:', error);
    throw error;
  }
};

export const createAllocation = async (allocationData: Omit<ResourceAllocation, 'id'>): Promise<ResourceAllocation> => {
  try {
    const response = await axios.post(`${API_URL}/resources/allocations/`, allocationData);
    return response.data;
  } catch (error) {
    console.error('Error creating resource allocation:', error);
    throw error;
  }
};

export const updateAllocation = async (id: number, allocationData: Partial<ResourceAllocation>): Promise<ResourceAllocation> => {
  try {
    const response = await axios.patch(`${API_URL}/resources/allocations/${id}/`, allocationData);
    return response.data;
  } catch (error) {
    console.error('Error updating resource allocation:', error);
    throw error;
  }
};

export const deleteAllocation = async (id: number): Promise<void> => {
  try {
    await axios.delete(`${API_URL}/resources/allocations/${id}/`);
  } catch (error) {
    console.error('Error deleting resource allocation:', error);
    throw error;
  }
};